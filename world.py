import matplotlib.pyplot as plt
from mold import Mold
import networkx as nx
import random
import time

class Food():
    def __init__(self, coords, size):
        self.coords = coords
        self.size = size

class World():
    def __init__(self, size=(100,100)):
        self.size = size
        self.food = {}
        
        self.place_food(0)

        self.mold = Mold((50,50), 10000, self.size)

    def place_food(self, num_food):
        seed = random.randint(1,100000)
        random.seed(42)

        for n in range(num_food):
            x = random.randint(0, self.size[0])
            y = random.randint(0, self.size[1])
            self.food[(x,y)] = random.randint(100,1000)

        random.seed(seed)

    def simulate(self, steps=100, framerate=10, display=False):
        if display:
            self.display()
            time.sleep(1)
        self.mold.new_tendril()
        
        for step in range(steps):
            frame_start = time.time()

            self.feed()
            self.mold.step()

            if display:
                self.display()
                elapsed = time.time() - frame_start
                frame_buffer = 1/framerate - elapsed
                if frame_buffer > 0:
                    time.sleep(frame_buffer)

    def feed(self):
        for food_coords, food_weight in list(self.food.items()):
            if self.mold.has_node(food_coords):
                print("feeding at (%d, %d)!" % food_coords)
                self.mold.set_node_weight(food_coords, self.mold.get_node_weight(food_coords)+min(10, food_weight))

                if food_weight <= 10:
                    self.food.pop(food_coords)
                else:
                    self.food[food_coords] -= 10

    def display(self):
        plt.clf()

        # plot border lines of grid
        corners_x = [0,self.size[0], self.size[0], 0, 0]
        corners_y = [0, 0, self.size[1], self.size[1], 0]
        plt.plot(corners_x, corners_y, color='black')

        # plot mold
        pos = nx.get_node_attributes(self.mold.G, 'pos')
        node_weights = list(nx.get_node_attributes(self.mold.G, 'weight').values())
        node_weights = [max(1, 100*(w/(1000))) for w in node_weights]
        node_color = [[138/255,54/255,31/255]] # brown
        nx.draw(self.mold.G, pos, node_size=node_weights, node_color=node_color, width=1)
        plt.title("fitness: "+str(self.mold.fitness()))
        plt.plot()

        plt.scatter([c[0] for c in self.food.keys()], [c[1] for c in self.food.keys()], s=list(self.food.values()), c='green')

        # allow rendering time
        plt.pause(0.01)        
