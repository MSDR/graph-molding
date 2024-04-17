import designed_worlds
import evolution
import glob
import matplotlib.pyplot as plt
import networkx as nx
import random
import utils
import world

display=True

# set up plt
if display:
    plt.ion()
    plt.figure(figsize=(10,10))
    plt.show(block=False)

# W = designed_worlds.gif_mold()
# W.simulate(steps=400, display=display)
#W = utils.load_world("worlds/test.pkl")

GA = evolution.GeneticAlgorithm(epochs=100, generation_size=100, world_function=designed_worlds.gif_mold, ckpt_folder='worlds/gif_mold/')
best_worlds = GA.run_algorithm()

### Genetic Algorithm Demo
# # # We will perform our Genetic Algorithm with its default parameters
# GA = evolution.GeneticAlgorithm(epochs=100)
# best_worlds = GA.run_algorithm()

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

# utils.save_world(W_best, "worlds/live_test/final.pkl")

### Evolution Demo
# for filepath in glob.glob("worlds/test/*.pkl"):
#     print("simulating", filepath)
#     W = utils.load_world(filepath)
#     W.simulate(steps=100, display=True)

if display:
    plt.ioff()