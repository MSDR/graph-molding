import networkx as nx
import numpy as np
import random
import utils

class Mold():
  ### core functionality ######################################################################################
    
    def __init__(self, center_coords, center_weight, world_size,
                 new_tendril_chance=0.05, new_tendril_weight=0.9,
                 tendril_branch_chance=0.1, tendril_branch_weight=0.9, tendril_branch_left_ratio=0.9,
                 tendril_extension_chance=0.8, tendril_extension_bend_stdev=0.3, tendril_extension_weight=0.9):
        self.G = nx.Graph()
        self.add_node(center_coords, center_weight)
        self.center_coords = center_coords
        self.world_size = world_size

        self.chromosome = {'new_tendril_chance':new_tendril_chance, #[0,1]
                           'new_tendril_weight':new_tendril_weight, #[0,1]. Proportion of center weight to pass to new tendril.
                           'tendril_branch_chance':tendril_branch_chance, #[0,1]
                           'tendril_branch_weight':tendril_branch_weight, #[0,1]. Proportion of leaf weight to pass to new leaves.
                           'tendril_branch_left_ratio':tendril_branch_left_ratio, #[0,1]. Proportion of branch weight to give to left branch.
                           'tendril_extension_chance':tendril_extension_chance, #[0,1]
                           'tendril_extension_bend_stdev':tendril_extension_bend_stdev, #[0,0.5], lower value means more bending.
                           'tendril_extension_weight':tendril_extension_weight} #[0,1]. Proportion of leaf weight to pass to new leaf.

    def step(self):
        tendril_leaves = self.find_tendril_leaves()
        for leaf in tendril_leaves:
            # branch or extend
            if random.random() < self.chromosome['tendril_branch_chance']:
                self.branch_tendril(leaf)
            elif random.random() < self.chromosome['tendril_extension_chance']:
                self.extend_tendril(leaf)

        # create new tendril from center
        if random.random() < self.chromosome['new_tendril_chance']:
            self.new_tendril()

    def fitness(self):
        return self.G.number_of_nodes()

  ### utility functions #######################################################################################

   ## direct mold functionality ########################
    def branch_tendril(self, leaf_coords):
        extension_coords = self.calculate_tendril_extension(leaf_coords)
        left_extension_coords = utils.move_on_3x3_square_perimeter(leaf_coords, extension_coords, -1)
        right_extension_coords = utils.move_on_3x3_square_perimeter(leaf_coords, extension_coords, 1)

        leaf_weight = self.get_node_weight(leaf_coords)

        if utils.coords_within_world(left_extension_coords, self.world_size):
            # calculate new weights for a left branch
            left_weight = leaf_weight*self.chromosome['tendril_branch_weight']*self.chromosome['tendril_branch_left_ratio']
            updated_leaf_weight = leaf_weight*(1-self.chromosome['tendril_branch_weight'])*(1-self.chromosome['tendril_branch_left_ratio'])

            # if new weights are large enough, branch left
            if left_weight >= 1 and updated_leaf_weight >= 1:
                self.add_node_edge(leaf_coords, left_extension_coords, updated_leaf_weight, left_weight)

        if utils.coords_within_world(right_extension_coords, self.world_size):
            # calculate new weights for a left branch
            right_weight = leaf_weight*self.chromosome['tendril_branch_weight']*(1-self.chromosome['tendril_branch_left_ratio'])
            updated_leaf_weight = leaf_weight*(1-self.chromosome['tendril_branch_weight'])*self.chromosome['tendril_branch_left_ratio']

            # if new weights are large enough, branch left
            if right_weight >= 1 and updated_leaf_weight >= 1:
                self.add_node_edge(leaf_coords, right_extension_coords, updated_leaf_weight, right_weight)

    
    # given a leaf node (deg == 1), extend a tendril in the same direction
    # this expects end_node as str
    def extend_tendril(self, leaf_coords):
        extension_coords = self.calculate_tendril_extension(leaf_coords)

        # calculate bend amount
        bend = max(min(int((random.random() - 0.5)/self.chromosome['tendril_extension_bend_stdev']), 7), -7)
        if bend > 0:
            extension_coords = utils.move_on_3x3_square_perimeter(leaf_coords, extension_coords, bend)

        if utils.coords_within_world(extension_coords, self.world_size):
            leaf_weight = self.get_node_weight(leaf_coords)

            # calculate new weights
            new_weight = leaf_weight*self.chromosome['new_tendril_weight']
            leaf_weight = leaf_weight*(1-self.chromosome['new_tendril_weight'])

            # if new weights are large enough, extend the tendril
            if new_weight >= 1 and leaf_weight >= 1:
                self.add_node_edge(leaf_coords, extension_coords, leaf_weight, new_weight)
                

    # creates a tendril from the center node, if an adjacent spot is unoccupied
    def new_tendril(self):
        # collect open adjacent coordinates
        open_directions = []
        for x in range(self.center_coords[0]-1, self.center_coords[0]+2):
            for y in range(self.center_coords[0]-1, self.center_coords[0]+2): 
                if (x,y) != self.center_coords and not self.G.has_node(utils.coords_to_str((x,y))):
                    open_directions.append((x,y))
        if len(open_directions) == 0:
            return
        
        # choose a direction to extend
        new_tendril_coords = random.choice(open_directions)

        if utils.coords_within_world(new_tendril_coords, self.world_size):  
            center_weight = self.get_node_weight(self.center_coords)

            # calculate new weights
            new_weight = center_weight*self.chromosome['new_tendril_weight']
            center_weight = center_weight*(1-self.chromosome['new_tendril_weight'])

            # if new weights are large enough, create new tendril
            if new_weight >= 1 and center_weight >= 1:
                self.add_node_edge(self.center_coords, new_tendril_coords, center_weight, new_weight)

   ## search within mold ###############################
    # all nodes with degree <= 1
    def find_tendril_leaves(self):
        return [node for node, d in self.G.degree() if d == 1]
    
    def calculate_tendril_extension(self, leaf_coords):
        neighbor = list(self.G.neighbors(leaf_coords))
                
        # calculate coords of new leaf
        leaf_x, leaf_y = utils.coords_to_tuple(leaf_coords)
        nbor_x, nbor_y = utils.coords_to_tuple(neighbor[0])
        return (leaf_x + (leaf_x - nbor_x), leaf_y + (leaf_y - nbor_y))
        

   ## nx wrappers ######################################
    # these all handle coords as tuple or str
        
    def add_node(self, coords, weight):
        pos = coords
        if type(coords) != str:
            coords = utils.coords_to_str(coords)
        else:
            pos = utils.coords_to_tuple(coords)
        
        if self.G.has_node(coords): # if coords exists, sum weight of existing node and new weight
            self.change_node_weight(coords, self.get_node_weight(coords)+weight)
        else:
            self.G.add_node(coords, pos=pos, weight=weight)

    def remove_node(self, coords):
        if type(coords) != str:
            coords = utils.coords_to_str(coords)
        
        self.G.remove_node(coords)

    def change_node_weight(self, coords, weight):
        if type(coords) != str:
            coords = utils.coords_to_str(coords)

        self.G.nodes[coords]['weight'] = weight

    def get_node_weight(self, coords):
        if type(coords) != str:
            coords = utils.coords_to_str(coords)

        return self.G.nodes[coords]['weight']

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
        self.add_node(new_node_coords, new_weight)
        self.add_edge(existing_node_coords, new_node_coords)
        self.change_node_weight(existing_node_coords, existing_weight)