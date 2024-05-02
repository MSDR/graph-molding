import designed_worlds
import evolution
import fitness_functions
import glob
import matplotlib.pyplot as plt
import networkx as nx
import random
import time
import utils
import world

display=True

### Interstate Demo
W = designed_worlds.interstate_map(fitness_function=fitness_functions.dense)
W.mold.chromosome = {'decay_rate':0.005, #[0,1]. Proportion of weight to decay at each step: -10*(1-decay_rate)
                    'differential_redist_ratio':0.8, #[0,1].
                    
                    'new_tendril_chance':0.1, #/100 = [0,0.01]. Chance per step to create new tendril from center.
                    'new_tendril_weight':0.5, #[0,1]. Proportion of center weight to pass to new tendril.
                    # node -- tube -- node
                    #           |
                    #          new

                    'tendril_branch_chance':0.3, #[0,1]. Chance per step per leaf to branch.
                    'tendril_branch_weight':0.9, #[0,1]. Proportion of leaf weight to pass to new leaves.
                    'tendril_branch_left_ratio':0.5, #[0,1]. Proportion of branch weight to give to left branch.
                    #   node
                    #     |
                    #   leaf
                    #   /  \
                    #  R    L

                    'tendril_extension_chance':0.7, #[0,1]. Chance per step per leaf to extend tendril if branch failed.
                    'tendril_extension_bend_stdev':0.5, #/2 = [0,0.5], lower value means more bending.
                    'tendril_extension_weight':0.9} #[0,1]. Proportion of leaf weight to pass to new leaf.
                    #   leaf  or  leaf  or   leaf -- new
                    #     |         \
                    #    new        new
W.simulate(steps=300, display=display)


## Genetic Algorithm Demo
# GA = evolution.GeneticAlgorithm(epochs=100, sim_steps=100, trials=3, mutation_rate=0.1, generation_size=100, success_ratio=0.1,
#                                 world_function=designed_worlds.interstate_map, fitness_function=fitness_functions.dense_with_food_cc_penalty, 
#                                 ckpt_folder='worlds/interstate/dense_with_food_cc_penalty/')
# best_worlds = GA.run_algorithm()

# # Once the Genetic Algorithm is done, we will select the best mold
# index = random.randint(0, len(best_worlds)-1)
# W_best = sorted(best_worlds, key = lambda w: w.fitness())[-1]

# # We will then calculate the fitness score
# W_best_fitness = W_best.fitness()

# # We will print the fitness score of the best mold world
# print("Fitness Score: %f" %(W_best_fitness))

# # We will then loop through the chromosomes and print their values
# chromosomes = W_best.mold.chromosome.keys()
# for chromosome in chromosomes:
#     print("%s: %f" %(chromosome, W_best.mold.chromosome[chromosome]))

# # We will then run the world of mold with display on and with the chromosome values that correspond to the best world
# W_best.simulate(steps=100, display=True)


### Evolution Demo
# for filepath in glob.glob("worlds/interstate/dense_with_food_cc_penalty/*.pkl"):
#     print("simulating", filepath)
#     W = utils.load_world(filepath)
#     W.simulate(steps=100, display=True)
#     print(W.fitness(), '\n')
