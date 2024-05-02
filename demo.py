import matplotlib.pyplot as plt
import mold_old
import networkx as nx
import utils
import world
import world_old

display=True

def convert_to_world_old(w):
    w_old = world_old.World(w.size, w.mold.center_coords, w.fitness_function, False,
                            w.num_random_food, w.random_food_range, w.init_food_coords)
    
    w_old.mold = mold_old.Mold(w.mold.center_coords, w.mold.starting_center_weight, w.mold.world_size)
    w_old.mold.chromosome = w.mold.chromosome
    w_old.reset()
    return w_old

def run_world(filepath, old=False, steps=100, wait=False):
    W = utils.load_world(filepath)
    if old:
        W = convert_to_world_old(W)

    print("simulating", filepath)
    W.simulate(steps=steps, display=True)
    print(" > fitness: %.2f\n" % W.fitness())

    if wait:
        input()

# dense: sum_weight/num_nodes
# run_world("old_worlds/interstate/dense/best.pkl", old=True, steps=200, wait=True)

# dense_with_food: dense*num_food_reached
# run_world("old_worlds/interstate/dense_with_food/best.pkl", old=True, steps=200, wait=True)

# densemax: sum_weight/max_weight

# densemax_with_food: densemax*food_reached
# run_world("old_worlds/interstate/densemax_with_food/best.pkl", old=True, steps=200, wait=True)



# dense_with_food: dense*num_food_reached
# run_world("worlds/interstate/dense_with_food/best.pkl", old=False, steps=200, wait=True)

# dense_with_food_cc_penalty: dense_with_food/(num_cc**2)
run_world("worlds/interstate/dense_with_food_cc_penalty/best.pkl", old=False, steps=200, wait=True)