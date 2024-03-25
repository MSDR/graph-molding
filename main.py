import matplotlib.pyplot as plt
import networkx as nx
import random
import world
import evolution

display=True

if display:
    # set up plt
    plt.ion()
    plt.figure(figsize=(10,10))
    plt.show(block=False)

# demoing the display
W = world.World()
W.simulate(display=display)

if display:
    plt.ioff()

# We will perform our Genetic Algorithm with its default parameters
GA = evolution.GeneticAlgorithm()
best_worlds = GA.run_algorithm()

# Once the Genetic Algorithm is done, we will select the best mold
index = random.randint(0, len(best_worlds)-1)
W_best = best_worlds[index]

# We will then run the world of mold with display on and with the chromosome values that correspond to the best world
W_best.simulate(steps=100, display=True)

# We will then calculate the fitness score
W_best_fitness = W_best.mold.fitness()

# We will print the fitness score of the best mold world
print("Fitness Score: %f" %(W_best_fitness))

# We will then loop through the chromosomes and print their values
chromosomes = W_best.mold.chromosome.keys()
for chromosome in chromosomes:
    print("%s: %f" %(chromosome, W_best.mold.chromosome[chromosome]))