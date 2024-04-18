import time
from designed_worlds import interstate_map
import utils
import glob
import networkx as nx
import math
import random

# # Displaying the interstate map
# W = interstate_map()
# print(W.mold.G.edges)
# W.display()
# time.sleep(10)

# for filepath in glob.glob("worlds\interstate\dense\*.pkl"):
#     print(filepath)

filepath = "worlds\interstate\dense\\20.pkl"
W = utils.load_world(filepath)
W.simulate(steps=100, display=True)
print(W.fitness())

G = W.mold.G

# Get the degree skew
pl_coefficient = 0.0

degrees = dict(nx.degree(G)).values()
min_degree = min(degrees)

d_sum = 0
for d in degrees:
  d_sum += math.log(d/min_degree)

pl_coefficient = 1 + len(degrees) / d_sum

print("Power-law coefficient:", round(pl_coefficient, 1))

# Small worldedness
avg_shortest_paths = 0.0

largest_component = max(nx.connected_components(G), key=len)

vertices = random.sample(list(largest_component), 10)

sum = 0
count = 0
longest = 0
for i in range(len(vertices)):
  for j in range(i+1, len(vertices)):
    l = nx.shortest_path_length(G, vertices[i], vertices[j])
    sum += l
    count += 1
    if l > longest:
      longest = l

avg_shortest_paths = sum / count

print("Average shortest path length:", round(avg_shortest_paths, 1))

# Diameter estimate of largest component
diameter = 0

diameter = longest

print("Diameter estimate:", diameter)
