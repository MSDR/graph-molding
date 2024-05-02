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

random.seed(11)

filepath = "worlds\\test\\best.pkl"
W = utils.load_world(filepath)
W.simulate(steps=200, display=False)
print(W.fitness())

G = W.mold.G

# Save a set of image
for i in range(10):
  W.simulate(steps=200, display=False)
  W.display("images/densemax_with_food_" + str(i))

# Get the largest component
largest_component = G.subgraph(max(nx.connected_components(G), key=len))

print("Largest component order:", largest_component.order())
print("Largest component size:", largest_component.size())
print()

# Get the degree skew of the largest component
pl_coefficient = 0.0

degrees = dict(nx.degree(largest_component)).values()
min_degree = min(degrees)

d_sum = 0
for d in degrees:
  d_sum += math.log(d/min_degree)

pl_coefficient = 1 + len(degrees) / d_sum

print("Power-law coefficient:", round(pl_coefficient, 3))
print()

# Small worldedness and diameter
avg_shortest_paths = 0.0

vertices = random.sample(list(largest_component.nodes), 20)

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

print("Average shortest path length:", round(avg_shortest_paths, 3))
print("Diameter estimate:", longest)
print()

# Get the k cores of the graph
cores = []

k = 0
while True:
  k_core = nx.k_core(largest_component, k=k)

  if k_core.order() == 0:
    break

  cores.append(k_core)
  k += 1

print("Largest core size:", k)
print("Largest core order:", cores[-1].order())
print("Largest core size:", cores[-1].size())
print()

# Get the k connectivity
k = 1
while nx.is_k_edge_connected(largest_component, k):
  k += 1
k -= 1

print("Maximum connectivity:", k)
print()

# Measures for centrality
DC_centers = nx.degree_centrality(largest_component)
CC_centers = nx.closeness_centrality(largest_component)
BC_centers = nx.betweenness_centrality(largest_component)
# EC_centers = nx.eigenvector_centrality(largest_component)

def sort_measures(Centers):
  ls = []
  for key in Centers:
    ls.append((key, Centers[key]))
  ls.sort(key=lambda x: x[1], reverse=True)
  ls = [item[0] for item in ls]
  return ls

DC_centers = sort_measures(DC_centers)
CC_centers = sort_measures(CC_centers)
BC_centers = sort_measures(BC_centers)
# EC_centers = sort_measures(EC_centers)

def top_nodes(G, centers):
  num_removed = 0
  G2 = nx.Graph(G)
  while nx.number_connected_components(G2) == 1:
    G2.remove_node(centers.pop(0))
    num_removed += 1

  return num_removed

num_removed_DC = top_nodes(largest_component, DC_centers)
num_removed_CC = top_nodes(largest_component, CC_centers)
num_removed_BC = top_nodes(largest_component, BC_centers)
# num_removed_EC = top_nodes(largest_component, EC_centers)

print("Degree centrality number to disconnect:", num_removed_DC)
print("Closeness centrality number to disconnect:", num_removed_CC)
print("Betweenness centrality number to disconnect:", num_removed_BC)
# print("Eigenvector centrality number to disconnect:", num_removed_EC)
