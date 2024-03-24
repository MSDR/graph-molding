import matplotlib.pyplot as plt
from mold import Mold
import networkx as nx
import time

class Food():
    def __init__(self, coords, size):
        self.coords = coords
        self.size = size

class World():
    def __init__(self, size=(100,100)):
        self.size = size
        self.food = self.place_food()
        self.mold = Mold((50,50), 10000, self.size)
        pass

    def place_food(self):
        pass

    def simulate(self, steps=100, framerate=10, display=False):
        self.display()
        time.sleep(1)
        self.mold.new_tendril()
        
        for step in range(steps):
            frame_start = time.time()

            self.mold.step()

            if display:
                self.display()
                elapsed = time.time() - frame_start
                frame_buffer = 1/framerate - elapsed
                if frame_buffer > 0:
                    time.sleep(frame_buffer)

    def display(self):
        plt.clf()

        # plot border lines of grid
        corners_x = [0,self.size[0], self.size[0], 0, 0]
        corners_y = [0, 0, self.size[1], self.size[1], 0]
        plt.plot(corners_x, corners_y, color='black')

        # plot mold
        pos = nx.get_node_attributes(self.mold.G, 'pos')
        node_weights = list(nx.get_node_attributes(self.mold.G, 'weight').values())
        node_weights = [max(1, 100*(w/(10000))) for w in node_weights]
        node_color = [[138/255,54/255,31/255]] # brown
        nx.draw(self.mold.G, pos, node_size=node_weights, node_color=node_color, width=1)
        plt.title("fitness: "+str(self.mold.fitness()))
        plt.plot()

        # allow rendering time
        plt.pause(0.01)        
