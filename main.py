import designed_worlds
import evolution
import fitness_functions
import glob
import matplotlib.pyplot as plt
import networkx as nx
import random
import utils
import world

display=True


### Interstate Demo
# W = designed_worlds.interstate_map()
# W.simulate(steps=40, display=display)


### Genetic Algorithm Demo
GA = evolution.GeneticAlgorithm(epochs=100, mutation_rate=0.1, generation_size=20, success_ratio=0.2,
                                world_function=designed_worlds.interstate_map, fitness_function=fitness_functions.num_nodes, 
                                ckpt_folder='worlds/interstate/')
best_worlds = GA.run_algorithm()

# Once the Genetic Algorithm is done, we will select the best mold
index = random.randint(0, len(best_worlds)-1)
W_best = sorted(best_worlds, key = lambda w: w.fitness())[-1]

# We will then calculate the fitness score
W_best_fitness = W_best.fitness()

# We will print the fitness score of the best mold world
print("Fitness Score: %f" %(W_best_fitness))

# We will then loop through the chromosomes and print their values
chromosomes = W_best.mold.chromosome.keys()
for chromosome in chromosomes:
    print("%s: %f" %(chromosome, W_best.mold.chromosome[chromosome]))

# We will then run the world of mold with display on and with the chromosome values that correspond to the best world
W_best.simulate(steps=100, display=True)


### Evolution Demo
# for filepath in glob.glob("worlds/interstate/*.pkl"):
#     print("simulating", filepath)
#     W = utils.load_world(filepath)
#     W.simulate(steps=100, display=True)
