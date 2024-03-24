import networkx as nx
import numpy as np
import random
import utils

class Mold():
  ### core functionality ######################################################################################
    
    def __init__(self, center_coords, center_weight, world_size,
                 new_tendril_chance=0.2, tendril_branch_chance=0.001, tendril_extension_chance=0.8, tendril_extension_bend_stdev=0.2):
        self.G = nx.Graph()
        self.add_node(center_coords, center_weight)
        self.center_coords = center_coords
        self.world_size = world_size

        self.chromosome = {'new_tendril_chance':new_tendril_chance, #[0,1]
                           'tendril_branch_chance':tendril_branch_chance, #[0,1]
                           'tendril_extension_chance':tendril_extension_chance, #[0,1]
                           'tendril_extension_bend_stdev':tendril_extension_bend_stdev} #[0,0.5], lower value means more bending

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
    def branch_tendril(self, leaf_coords, left_node_weight=50, right_node_weight=50):
        extension_coords = self.calculate_tendril_extension(leaf_coords)
        left_extension_coords = utils.move_on_3x3_square_perimeter(leaf_coords, extension_coords, -1)
        right_extension_coords = utils.move_on_3x3_square_perimeter(leaf_coords, extension_coords, 1)

        # extend the tendril
        if utils.coords_within_world(left_extension_coords, self.world_size):
            self.add_node_edge(leaf_coords, left_extension_coords, left_node_weight)
        if utils.coords_within_world(right_extension_coords, self.world_size):
            self.add_node_edge(leaf_coords, right_extension_coords, right_node_weight)
    
    # given a leaf node (deg == 1), extend a tendril in the same direction
    # this expects end_node as str
    def extend_tendril(self, leaf_coords, node_weight=50, edge_weight=5):
        extension_coords = self.calculate_tendril_extension(leaf_coords)

        # calculate bend amount
        bend = max(min(int((random.random() - 0.5)/self.chromosome['tendril_extension_bend_stdev']), 7), -7)
        if bend > 0:
            extension_coords = utils.move_on_3x3_square_perimeter(leaf_coords, extension_coords, bend)

        # extend the tendril
        if utils.coords_within_world(extension_coords, self.world_size):
            self.add_node_edge(leaf_coords, extension_coords, node_weight)

    # creates a tendril from the center node, if an adjacent spot is unoccupied
    def new_tendril(self, node_weight=50, edge_weight=5):
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

        # extend
        if utils.coords_within_world(new_tendril_coords, self.world_size):  
            self.add_node_edge(self.center_coords, new_tendril_coords, node_weight)

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
        if type(coords) != str:
            str_coords = utils.coords_to_str(coords)
            self.G.add_node(str_coords, pos=coords, weight=weight)
        else:
            tuple_coords = utils.coords_to_tuple(coords)
            self.G.add_node(coords, pos=tuple_coords, weight=weight)

    def remove_node(self, coords):
        if type(coords) != str:
            coords = utils.coords_to_str(coords)
        
        self.G.remove_node(coords)

    def add_node_edge(self, existing_node_coords, new_node_coords, weight):
        self.add_node(new_node_coords, weight)
        self.add_edge(existing_node_coords, new_node_coords)

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