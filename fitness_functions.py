import mold

### fitness functions #######################################################################################

# sum of node weights
def sum_weight(mold):
        return sum([mold.get_node_weight(n) for n in mold.G.nodes()])
    
# number of nodes
def num_nodes(mold):
    return mold.G.number_of_nodes()