import copy
import networkx as nx
import numpy as np
import random
import utils

class Mold():
  ### core functionality ######################################################################################
    
    def __init__(self, center_coords, starting_center_weight, world_size,
                 decay_rate=0.9, differential_redist_ratio_older=0.7, differential_redist_ratio_younger=0.5,
                 new_tendril_chance=0.005, new_tendril_weight=0.5,
                 tendril_branch_chance=0.3, tendril_branch_weight=0.9, tendril_branch_left_ratio=0.5,
                 tendril_extension_chance=0.6, tendril_extension_bend_stdev=0.4, tendril_extension_weight=0.9):
        
        self.G = nx.Graph()

        self.add_node(center_coords, int(starting_center_weight))
        self.starting_center_weight = starting_center_weight
        self.center_coords = center_coords

        self.frozen_G = None
        self.freeze_G()

        self.world_size = world_size

        self.food_reached = []

        self.chromosome = {'decay_rate':decay_rate, #[0,1]. Proportion of weight to decay at each step. TODO
                           'differential_redist_ratio_older':differential_redist_ratio_older, #[0,1], [0,0.5) propagates weight outwards, (0.5,1] inwards.
                           'differential_redist_ratio_younger':differential_redist_ratio_younger,
                           # 10-20-10 -> 15-10-15 with ratio=0.5 
                           
                           'new_tendril_chance':new_tendril_chance, #[0,1]. Chance per step to create new tendril from center.
                           'new_tendril_weight':new_tendril_weight, #[0,1]. Proportion of center weight to pass to new tendril.
                           # center
                           #    |
                           #   new

                           'tendril_branch_chance':tendril_branch_chance, #[0,1]. Chance per step per leaf to branch.
                           'tendril_branch_weight':tendril_branch_weight, #[0,1]. Proportion of leaf weight to pass to new leaves.
                           'tendril_branch_left_ratio':tendril_branch_left_ratio, #[0,1]. Proportion of branch weight to give to left branch.
                           #   leaf
                           #   /  \
                           #  R    L

                           'tendril_extension_chance':tendril_extension_chance, #[0,1]. Chance per step per leaf to extend tendril if branch failed.
                           'tendril_extension_bend_stdev':tendril_extension_bend_stdev, #[0,0.5], lower value means more bending.
                           'tendril_extension_weight':tendril_extension_weight} #[0,1]. Proportion of leaf weight to pass to new leaf.
                            #   leaf  leaf   leaf-new
                            #     |      \
                            #    new     new

    def step(self):
        self.age()
        self.decay()
        self.distribute_weight()

        # branch or extend
        tendril_leaves = self.find_tendril_leaves()
        for leaf in tendril_leaves:
            if random.random() < self.chromosome['tendril_branch_chance']:
                self.branch_tendril(leaf)
            elif random.random() < self.chromosome['tendril_extension_chance']:
                self.extend_tendril(leaf)
        

        # create new tendril from non-leaves
        for node in set(self.G.nodes)-tendril_leaves:
            if len(list(self.G.neighbors(node))) == 2:
                if random.random() < self.chromosome['new_tendril_chance']:
                    self.new_tendril(node)



  ### utility functions #######################################################################################

   ## direct mold functionality ########################
    def age(self):
        for node, ddata in list(self.G.nodes(data=True)):
            ddata['age'] += 1

    def decay(self):
        nodes = list(self.G.nodes())
        for node in nodes:

            weight = self.get_node_weight(node)
            if weight < 1:
                self.remove_node(node)
            else:
                decay_amount = int((self.get_node_age(node)/10*(1-max(0, self.chromosome['decay_rate']))))
                decay_amount = max(0, min(10, decay_amount))
                self.set_node_weight(node, weight-decay_amount)


    def distribute_weight(self):
        self.freeze_G()

        for node in list(self.G.nodes()):
            node_weight = self.frozen_G.nodes[node]['weight']
            node_age = self.frozen_G.nodes[node]['age']

            # {neighbor:neighbor_weight}
            # only consider neighbors with smaller weight
            neighbors = {(nbor,self.frozen_G.nodes[nbor]['weight'],self.frozen_G.nodes[nbor]['age']) for nbor in list(self.G.neighbors(node)) if self.frozen_G.nodes[nbor]['weight'] < node_weight}
            sorted_neighbors = sorted([(nbor, nbor_weight, nbor_age) for nbor, nbor_weight, nbor_age in neighbors], key=lambda l: (l[2], l[1]), reverse=True)

            # distribute weight based on ratio of weight differential        
            given_older = False    
            for nbor, nbor_weight, nbor_age in sorted_neighbors:
                
                # if not given_older and nbor_age > self.get_node_age(node):
                #     weight_diff = int((node_weight - nbor_weight)*self.chromosome['differential_redist_ratio_older'])
                #     given_older = True
                # else:
                #     weight_diff = int((node_weight - nbor_weight)*self.chromosome['differential_redist_ratio_younger'])
                weight_diff = int((node_weight - nbor_weight)*self.chromosome['differential_redist_ratio_older'])

                old_total = self.get_node_weight(node) + self.get_node_weight(nbor)
                if self.get_node_weight(node) - weight_diff > 1:
                    self.set_node_weight(node, self.get_node_weight(node) - weight_diff)
                    self.set_node_weight(nbor, self.get_node_weight(nbor) + weight_diff)
                    new_total = self.get_node_weight(node) + self.get_node_weight(nbor)

                    #if new_total - old_total > 0.000001:
                        #print("problem! new: %f, old: %f" % (new_total, old_total))


    def branch_tendril(self, leaf_coords):
        extension_coords = self.calculate_tendril_extension(leaf_coords)
        left_extension_coords = utils.move_on_3x3_square_perimeter(leaf_coords, extension_coords, -1)
        right_extension_coords = utils.move_on_3x3_square_perimeter(leaf_coords, extension_coords, 1)

        leaf_weight = self.get_node_weight(leaf_coords)

        if utils.coords_within_world(left_extension_coords, self.world_size):
            # calculate new weights for a left branch
            left_weight = int(leaf_weight*self.chromosome['tendril_branch_weight']*self.chromosome['tendril_branch_left_ratio'])
            updated_leaf_weight = self.get_node_weight(leaf_coords) - left_weight

            # if new weights are large enough, branch left
            if left_weight >= 1 and updated_leaf_weight >= 1:
                self.add_node_edge(leaf_coords, left_extension_coords, updated_leaf_weight, left_weight)

        if utils.coords_within_world(right_extension_coords, self.world_size):
            # calculate new weights for a left branch
            right_weight = int(leaf_weight*self.chromosome['tendril_branch_weight']*(1-self.chromosome['tendril_branch_left_ratio']))
            updated_leaf_weight = self.get_node_weight(leaf_coords) - right_weight

            # if new weights are large enough, branch left
            if right_weight >= 1 and updated_leaf_weight >= 1:
                self.add_node_edge(leaf_coords, right_extension_coords, updated_leaf_weight, right_weight)

    
    # given a leaf node (deg == 1), extend a tendril in the same direction
    # this expects end_node as str
    def extend_tendril(self, leaf_coords):
        extension_coords = self.calculate_tendril_extension(leaf_coords)

        # calculate bend amount
        bend = max(min(int((random.random() - 0.5)/self.chromosome['tendril_extension_bend_stdev']), 7), -7)
        if bend != 0:
            extension_coords = utils.move_on_3x3_square_perimeter(leaf_coords, extension_coords, bend)

        if utils.coords_within_world(extension_coords, self.world_size):
            leaf_weight = self.get_node_weight(leaf_coords)

            # calculate new weights
            new_weight = int(leaf_weight*self.chromosome['new_tendril_weight'])
            leaf_weight = leaf_weight - new_weight

            # if new weights are large enough, extend the tendril
            if new_weight >= 1 and leaf_weight >= 1:
                self.add_node_edge(leaf_coords, extension_coords, leaf_weight, new_weight)


    # creates a tendril from the center node, if an adjacent spot is unoccupied
    def new_tendril(self, source_coords):
        if type(source_coords) != tuple:
            source_coords = utils.coords_to_tuple(source_coords)

        # collect open adjacent coordinates
        open_directions = []
        for x in range(source_coords[0]-1, source_coords[0]+2):
            for y in range(source_coords[1]-1, source_coords[1]+2): 
                if (x,y) != source_coords and not self.G.has_node(utils.coords_to_str((x,y))):
                    open_directions.append((x,y))
        if len(open_directions) == 0:
            return
        
        # choose a direction to extend
        new_tendril_coords = random.choice(open_directions)

        if utils.coords_within_world(new_tendril_coords, self.world_size):  
            source_weight = self.get_node_weight(source_coords)

            # calculate new weights
            new_weight = int(source_weight*self.chromosome['new_tendril_weight'])
            source_weight = source_weight - new_weight

            # if new weights are large enough, create new tendril
            if new_weight >= 1 and source_weight >= 1:
                self.add_node_edge(source_coords, new_tendril_coords, source_weight, new_weight)

    # stores a copy of self.G in self.frozen_G
    def freeze_G(self):
        self.frozen_G = copy.deepcopy(self.G)

   ## search within mold ###############################
    # all nodes with degree <= 1
    def find_tendril_leaves(self):
        return {node for node, d in self.G.degree() if d == 1}
    
    def calculate_tendril_extension(self, leaf_coords):
        neighbor = list(self.G.neighbors(leaf_coords))
                
        # calculate coords of new leaf
        leaf_x, leaf_y = utils.coords_to_tuple(leaf_coords)
        nbor_x, nbor_y = utils.coords_to_tuple(neighbor[0])
        return (leaf_x + (leaf_x - nbor_x), leaf_y + (leaf_y - nbor_y))
    
    def reset_G(self):
        self.G = nx.Graph()

        self.add_node(self.center_coords, int(self.starting_center_weight))

        self.frozen_G = None
        self.freeze_G()
        

   ## nx wrappers ######################################
    # these all handle coords as tuple or str
        
    def add_node(self, coords, weight):
        pos = coords
        if type(coords) != str:
            coords = utils.coords_to_str(coords)
        else:
            pos = utils.coords_to_tuple(coords)
        
        if self.G.has_node(coords): # if coords exists, sum weight of existing node and new weight
            self.set_node_weight(coords, self.get_node_weight(coords)+weight)
        else:
            self.G.add_node(coords, pos=pos, weight=weight, age=1)

    def remove_node(self, coords):
        if type(coords) != str:
            coords = utils.coords_to_str(coords)
        
        self.G.remove_node(coords)

    def has_node(self, coords):
        if type(coords) != str:
            coords = utils.coords_to_str(coords)
        
        return self.G.has_node(coords)
    
    def get_node_age(self, coords):
        if type(coords) != str:
            coords = utils.coords_to_str(coords)

        return self.G.nodes[coords]['age']

    def get_node_weight(self, coords):
        if type(coords) != str:
            coords = utils.coords_to_str(coords)

        return self.G.nodes[coords]['weight']

    def set_node_weight(self, coords, weight):
        if type(coords) != str:
            coords = utils.coords_to_str(coords)

        self.G.nodes[coords]['weight'] = weight
        

    def add_edge(self, coords_u, coords_v):
        if type(coords_u) != str:
            coords_u = utils.coords_to_str(coords_u)
        if type(coords_v) != str:
            coords_v = utils.coords_to_str(coords_v)

        self.G.add_edge(coords_u, coords_v)

    def remove_edge(self, coords_u, coords_v):
        if type(coords_u) != str:
            coords_u = utils.coords_to_str(coords_u)
        if type(coords_v) != str:
            coords_v = utils.coords_to_str(coords_v)

        self.G.remove_edge(coords_u, coords_v)

    def add_node_edge(self, existing_node_coords, new_node_coords, existing_weight, new_weight):
        if type(existing_node_coords) != str:
            existing_node_coords = utils.coords_to_str(existing_node_coords)
        if type(new_node_coords) != str:
            new_node_coords = utils.coords_to_str(new_node_coords)

        self.add_node(new_node_coords, new_weight)
        self.add_edge(existing_node_coords, new_node_coords)
        self.set_node_weight(existing_node_coords, existing_weight)