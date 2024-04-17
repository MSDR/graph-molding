import mold

### fitness functions #######################################################################################

# sum of node weights
def sum_weight(mold):
    return sum([mold.get_node_weight(n) for n in mold.G.nodes()])
    
# number of nodes
def num_nodes(mold):
    return mold.G.number_of_nodes()

def dense(mold):
    n = num_nodes(mold)
    return sum_weight(mold)/(n if n > 0 else 1)