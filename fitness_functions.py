import mold
import networkx as nx

### fitness functions #######################################################################################

# sum of node weights
def sum_weight(mold):
    return sum([mold.get_node_weight(n) for n in mold.G.nodes()])
    
# number of nodes
def num_nodes(mold):
    return mold.G.number_of_nodes()

# sum_weight / max(1, num_nodes)
def dense(mold):
    n = num_nodes(mold)
    return sum_weight(mold)/max(1, n)

# max(1, number of food reached)
def food_reached(mold):
    return max(len(mold.food_reached), 1)

# dense * food_reached
def dense_with_food(mold):
    dense_ = dense(mold)
    food_reached_ = food_reached(mold)
    return dense_*food_reached_

# dense_with_food / (number_connected_components**2)
def dense_with_food_cc_penalty(mold):
    dense_with_food_ = dense_with_food(mold)
    num_connected_components = max(1, nx.number_connected_components(mold.G))
    return dense_with_food_/(num_connected_components**2)

# (sum weight / max weight) * max(1, num food reached)
# returns 0 if mold has 0 nodes
def densemax_with_food(mold):
    nodes = mold.G.nodes()
    if len(nodes) == 0:
        return 0
    
    max_weight = sorted([mold.get_node_weight(n) for n in nodes])[-1]
    dense = sum_weight(mold)/max(max_weight, 1)
    food_reached = max(len(mold.food_reached), 1)
    return dense*food_reached