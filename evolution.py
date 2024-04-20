import copy
import designed_worlds
import fitness_functions
from pathlib import Path
import random
import utils
import world

class GeneticAlgorithm():
    def __init__(self, epochs = 100, sim_steps=100, trials=10, mutation_rate=0.05, generation_size=10, success_ratio=0.2, 
                 world_function=designed_worlds.random_500, fitness_function=fitness_functions.num_nodes,
                 ckpt_folder=None, ckpt_interval=10):
        # simulation parameters
        self.epochs = epochs
        self.sim_steps = sim_steps
        self.trials = trials

        # rate of mutation per gene btw [0,1]
        self.mutation_rate = mutation_rate

        # number of molds per generation
        self.generation_size = generation_size

        # percent of top performing parents for next generation
        self.success_ratio = success_ratio

        # function to generate new worlds
        self.world_function = world_function

        # function to use for fitness evaluation
        self.fitness_function = fitness_function

        # list of worlds, each with their own single mold
        self.generation = self.first_generation(generation_size)

        # checkpoint info
        self.ckpt_interval = ckpt_interval
        self.ckpt_folder = ckpt_folder # leave as None to not save checkpoints
        if self.ckpt_folder is not None:
            Path(self.ckpt_folder).mkdir(parents=True, exist_ok=True)

    # populates first generation of worlds
    def first_generation(self, generation_size):
        # We will have a list of molds that we will consider as our generation set
        generational_molds = []

        # We will create 'generation_size' worlds of molds
        for generation in range(generation_size):
            # We will create a new world
            new_world = self.world_function(fitness_function=self.fitness_function)
            
            # We will then loop through every chromosome and set a random value
            chromosomes = new_world.mold.chromosome.keys()
            for chromosome in chromosomes:
                new_world.mold.chromosome[chromosome] = random.random()

            # We will then append it to the total list of molds
            generational_molds.append(new_world)

        return generational_molds


    # I mean....you know what it is
    def sex(self, parent1, parent2):
        # We will create a child world that will contain combination of chromosome values from parents 1 and 2
        child_world = self.world_function(fitness_function=self.fitness_function)

        # For each chromosome in the child mold, we will set the chromosome values
        chromosome = child_world.mold.chromosome.keys()
        for gene in chromosome:

            # If we are less than the mutation rate, then we simply initialize the gene at a random value
            if random.random() < self.mutation_rate:
                child_world.mold.chromosome[gene] = random.random()

            # Else, we will take the gene value from either parent 1 or parent 2
            else:
                # If we randomly select 0, we will take the gene value from parent 1
                if random.randint(0, 1) == 0:
                    child_world.mold.chromosome[gene] = parent1.mold.chromosome[gene]
                # If we randomly select 1, we will take the gene value from parent 2
                else:
                    child_world.mold.chromosome[gene] = parent2.mold.chromosome[gene]
        self.generation.append(child_world)


    # Run the Genetic Algorithm a 'epochs' amount of times. We will return a list of molds with optimized chromosome values
    def run_algorithm(self):
        # We will loop over the number of epochs
        best_fitness = -float('inf')
        for epoch in range(1,self.epochs+1):
            # We will perform an iteration of the Genetic Algorithm, which is defined as step
            self.step() 

            # take top performers as parents
            self.generation.sort(key=lambda w: sum(w.last_fitnesses)/len(w.last_fitnesses), reverse=True)
            parents = copy.deepcopy(self.generation[0:int(self.generation_size*self.success_ratio)+1])

            best_world = self.generation[0]
            best_world_fitness = sum(best_world.last_fitnesses)/len(best_world.last_fitnesses)

            print("epoch %d, avg. last fitness: %.2f" % (epoch, best_world_fitness))

            # save best world
            if best_world_fitness > best_fitness:
                best_fitness = best_world_fitness
                utils.save_world(best_world, self.ckpt_folder+"best.pkl")
                print("..saving new best at epoch %d! avg. last fitness: %.2f" % (epoch, best_world_fitness))

            # save checkpoint
            if (self.ckpt_folder is not None) and (epoch == 1 or epoch % self.ckpt_interval == 0):
                utils.save_world(best_world, self.ckpt_folder+str(epoch)+".pkl")
                print("...saving epoch %d checkpoint. avg. last fitness: %.2f" % (epoch, best_world_fitness))

            # We will reset the generation set
            self.generation = []

            # We will loop through the parents of the world
            for worlds in parents:
                # We will reset the world
                worlds.reset()

                # We will then append the parent freshly reset in the list of generations
                self.generation.append(worlds)

            # We will then repopulate the generation set until we have a size of 'generation_size'
            while len(self.generation) < self.generation_size:
                # We will compute index 1 and 2 that will represent parents 1 and 2
                index1 = random.randint(0, len(parents)-1)
                index2 = random.randint(0, len(parents)-1)
                while index1 == index2:
                    index2 = random.randint(0, len(parents)-1)

                # We will then perform...hehehehehe
                self.sex(parents[index1], parents[index2])

        return self.generation
    

    # one iteration
    def step(self):
        for trial in range(self.trials):
            for world in self.generation:
                world.reset(reset_best_fitness=False, reset_last_fitnesses=False)
                world.simulate(steps=self.sim_steps)