import matplotlib.pyplot as plt
from mold import Mold
import networkx as nx

class Food():
    def __init__(self, coords, size):
        self.coords = coords
        self.size = size

class World():
    def __init__(self, size=(100,100)):
        self.size = size
        self.food = []
        self.mold = Mold((50,50), 200)
        pass

    def place_food(self):
        pass

    def simulate(self, mold, steps):
        pass

    def display(self):
        # plot border lines of grid
        corners_x = [0,self.size[0], self.size[0], 0, 0]
        corners_y = [0, 0, self.size[1], self.size[1], 0]
        plt.plot(corners_x, corners_y, color='black')

        # plot mold
        pos = nx.get_node_attributes(self.mold.G, 'pos')
        node_weights = list(nx.get_node_attributes(self.mold.G, 'weight').values())
        edge_weights = list(nx.get_edge_attributes(self.mold.G, 'weight').values())
        edge_weights = [w/5 for w in edge_weights]
        node_color = [[138/255,54/255,31/255]] # brown
        nx.draw(self.mold.G, pos, node_size=node_weights, node_color=node_color, width=edge_weights)
        plt.plot()

        # allow rendering time
        plt.pause(0.01)        
