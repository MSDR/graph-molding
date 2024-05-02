import time
from designed_worlds import interstate_map
import utils
import glob
import networkx as nx
import math
import random
import world_old
import mold_old

def convert_to_world_old(w):
    w_old = world_old.World(w.size, w.mold.center_coords, w.fitness_function, False,
                            w.num_random_food, w.random_food_range, w.init_food_coords)
    
    w_old.mold = mold_old.Mold(w.mold.center_coords, w.mold.starting_center_weight, w.mold.world_size)
    w_old.mold.chromosome = w.mold.chromosome
    w_old.reset()
    return w_old

# # Displaying the interstate map
# W = interstate_map()
# print(W.mold.G.edges)
# W.display()
# time.sleep(10)

# for filepath in glob.glob("worlds\interstate\dense\*.pkl"):
#     print(filepath)

# random.seed(11)

filepath = "old_worlds/interstate/densemax_with_food/best.pkl"
W = utils.load_world(filepath)
# W = convert_to_world_old(W)
W.simulate(steps=200, display=False)
print(W.fitness())
G = W.mold.G

# Save a set of image
# for i in range(10):
#   W = utils.load_world(filepath)
#   # W = convert_to_world_old(W)
#   W.simulate(steps=200, display=False)
#   W.display("dense_with_food" + str(i))

ITERATIONS=4
filepaths = [
            # "old_worlds/interstate/dense/best.pkl",
            # "old_worlds/interstate/densemax_with_food/best.pkl",
            # "worlds/interstate/dense_with_food/best.pkl",
            "worlds/interstate/dense_with_food_cc_penalty/best.pkl"
          ]

for filepath in filepaths:
  print(filepath)

  average_largest_component = 0
  average_pl = 0
  average_path = 0
  average_diameter = 0
  average_k_core = 0
  average_k_conn = 0
  for i in range(ITERATIONS):
    random.seed(i)
    print("i: ", i)
    W = utils.load_world(filepath)
    if "old" in filepath:
      W = convert_to_world_old(W)
    W.simulate(steps=200, display=False)
    G = W.mold.G

    # Get the largest component
    largest_component = G.subgraph(max(nx.connected_components(G), key=len))

    # print("Largest component order:", largest_component.order())
    # print("Largest component size:", largest_component.size())
    # print()

    # Get the degree skew of the largest component
    pl_coefficient = 0.0

    degrees = dict(nx.degree(largest_component)).values()
    min_degree = min(degrees)

    d_sum = 0
    if len(degrees) > 1:
      for d in degrees:
        d_sum += math.log(d/max(1, min_degree))

    pl_coefficient = 1 + len(degrees) / max(d_sum, 1)

    # print("Power-law coefficient:", round(pl_coefficient, 3))
    # print()

    # k cores
    cores = []

    k = 0
    while True:
      k_core = nx.k_core(largest_component, k=k)

      if k_core.order() == 0:
        break

      cores.append(k_core)
      k += 1

    average_k_core += k

    # Get the k connectivity
    k = 1
    while nx.is_k_edge_connected(largest_component, k):
      k += 1
    k -= 1

    average_k_conn += k


    average_largest_component += largest_component.order()
    average_pl += pl_coefficient
    average_path += nx.average_shortest_path_length(largest_component)
    average_diameter += nx.diameter(largest_component)
    print()


  print("largest component:", int(average_largest_component/ITERATIONS))
  print("pl:", average_pl/ITERATIONS)
  print("average path:", average_path/ITERATIONS)
  print("average diameter:", average_diameter/ITERATIONS)
  print("average k core:", average_k_core/ITERATIONS)
  print("average_k_conn:", average_k_conn/ITERATIONS)
  print()

# # Get the k cores of the graph
# cores = []

# k = 0
# while True:
#   k_core = nx.k_core(largest_component, k=k)

#   if k_core.order() == 0:
#     break

#   cores.append(k_core)
#   k += 1

# print("Largest core size:", k)
# print("Largest core order:", cores[-1].order())
# print("Largest core size:", cores[-1].size())
# print()

# # Get the k connectivity
# k = 1
# while nx.is_k_edge_connected(largest_component, k):
#   k += 1
# k -= 1

# print("Maximum connectivity:", k)
# print()

# # Measures for centrality
# DC_centers = nx.degree_centrality(largest_component)
# CC_centers = nx.closeness_centrality(largest_component)
# BC_centers = nx.betweenness_centrality(largest_component)
# # EC_centers = nx.eigenvector_centrality(largest_component)

# def sort_measures(Centers):
#   ls = []
#   for key in Centers:
#     ls.append((key, Centers[key]))
#   ls.sort(key=lambda x: x[1], reverse=True)
#   ls = [item[0] for item in ls]
#   return ls

# DC_centers = sort_measures(DC_centers)
# CC_centers = sort_measures(CC_centers)
# BC_centers = sort_measures(BC_centers)
# # EC_centers = sort_measures(EC_centers)

# def top_nodes(G, centers):
#   num_removed = 0
#   G2 = nx.Graph(G)
#   while nx.number_connected_components(G2) == 1:
#     G2.remove_node(centers.pop(0))
#     num_removed += 1

#   return num_removed

# num_removed_DC = top_nodes(largest_component, DC_centers)
# num_removed_CC = top_nodes(largest_component, CC_centers)
# num_removed_BC = top_nodes(largest_component, BC_centers)
# # num_removed_EC = top_nodes(largest_component, EC_centers)

# print("Degree centrality number to disconnect:", num_removed_DC)
# print("Closeness centrality number to disconnect:", num_removed_CC)
# print("Betweenness centrality number to disconnect:", num_removed_BC)
# # print("Eigenvector centrality number to disconnect:", num_removed_EC)
