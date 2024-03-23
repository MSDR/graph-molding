import networkx as nx
import utils

class Mold():
  ### core functionality ######################################################################################
    
    def __init__(self, center_coords, center_weight):
        self.G = nx.Graph()
        self.add_node(center_coords, center_weight)

    def step(self):
        pass

    def fitness(self):
        pass

  ### utility functions #######################################################################################
    # all coords are tuple (x,y)

    def add_node(self, coords, weight):
        self.G.add_node(utils.coords_to_str(coords), pos=coords, weight=weight)

    def remove_node(self, coords):
        self.G.remove_node(utils.coords_to_str(coords))

    def move_node(self, old_coords, new_coords):
        self.G = nx.relabel_nodes(self.G, {utils.coords_to_str(old_coords):utils.coords_to_str(new_coords)})

    def add_edge(self, coords_u, coords_v, weight):
        self.G.add_edge(utils.coords_to_str(coords_u), utils.coords_to_str(coords_v), weight=weight)

    def remove_edge(self, coords_u, coords_v):
        self.G.remove_edge(utils.coords_to_str(coords_u), utils.coords_to_str(coords_v))