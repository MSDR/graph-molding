import fitness_functions
import matplotlib.pyplot as plt
import mold
from mold import Mold
import networkx as nx
import random
import time

class World(object):
    def __init__(self, size=(100,100), mold_pos=(50,50), fitness_function=fitness_functions.sum_weight):
        self.size = size
        self.food = {}
        
        self.absorption_rate = 100
        self.mold = Mold(mold_pos, 10000, self.size)
        self.fitness_function = fitness_function

    # places food into the world
    # num_random is number of foods to place at random coordinates
    # food_coords, a list of ((x,y), size) tuples, places food at provided coordinates
    def place_food(self, num_random=0, random_range_min=100, random_range_max=1000, food_coords=[], seed=None):
        if seed == None:
            seed = random.randint(1,100000)
        random.seed(seed)

        for n in range(num_random):
            x = random.randint(0, self.size[0])
            y = random.randint(0, self.size[1])
            self.food[(x,y)] = random.randint(random_range_min,random_range_max)

        for coords, size in food_coords:
            self.food[coords] = size

        random.seed(seed)

    # run full simulation
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

            if self.mold.G.number_of_nodes == 0:
                return

    # absorb food into overlapping nodes
    def feed(self):
        for food_coords, food_weight in list(self.food.items()):
            if self.mold.has_node(food_coords):
                self.mold.set_node_weight(food_coords, self.mold.get_node_weight(food_coords)+min(self.absorption_rate, food_weight))

                if food_weight <= self.absorption_rate:
                    self.food.pop(food_coords)
                else:
                    self.food[food_coords] -= self.absorption_rate

    # display (in a separate window)
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
        plt.title("fitness: "+str(self.fitness_function(self.mold)))
        plt.plot()

        food_sizes = [max(1, 100*(f/1000)) for f in list(self.food.values())]
        plt.scatter([c[0] for c in self.food.keys()], [c[1] for c in self.food.keys()], s=food_sizes, c='green')

        # allow rendering time
        plt.pause(0.01)       

    def reset(self):
        self.mold.reset_G()
        self.food = {}
        self.place_food()

    def fitness(self):
        return self.fitness_function(self.mold)