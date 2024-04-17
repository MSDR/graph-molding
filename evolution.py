import designed_worlds
import fitness_functions
import random
import utils
import world

class GeneticAlgorithm():
    def __init__(self, epochs = 100, sim_steps=100, mutation_rate=0.05, generation_size=10, success_ratio=0.2, 
                 world_function=designed_worlds.random_500, fitness_function=fitness_functions.num_nodes,
                 ckpt_folder=None):
        # number of full simulations to run
        self.epochs = epochs

        self.sim_steps = sim_steps

        # rate of mutation per gene btw [0,1]
        self.mutation_rate = mutation_rate

        # number of molds per generation
        self.generation_size = generation_size

        # percent of top performing parents for next generation
        self.success_ratio = success_ratio

        # function to generate new worlds
        self.world_function = world_function

        self.fitness_function = fitness_function

        # list of worlds, each with their own single mold
        self.generation = self.first_generation(generation_size)

        # leave as None to not save checkpoints
        self.ckpt_folder=ckpt_folder
        self.best_fitness=-float('inf')

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
                if chromosome == 'decay_rate':
                    new_world.mold.chromosome[chromosome] = 0.01
                elif chromosome == 'tendril_extension_bend_stdev':
                    new_world.mold.chromosome[chromosome]/=2
                else:
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
                if gene == 'tendril_extension_bend_stdev':
                    child_world.mold.chromosome[gene]/=2
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
        for epoch in range(self.epochs):
            # We will perform an iteration of the Genetic Algorithm, which is defined as step
            self.step() 

            # TODO: this doesn't work because self.generation hasn't simulated yet
            best_world = sorted(self.generation, key = lambda w: w.fitness())[-1]
            best_world_fitness = best_world.fitness()

            # save best world
            if best_world_fitness > best_fitness:
                best_fitness = best_world_fitness
                utils.save_world(best_world, self.ckpt_folder+"best.pkl")
                print("..saving new best at epoch %d! fitness: %.2f" % (epoch, best_world_fitness))

            # save checkpoint
            if epoch % 10 == 0 and self.ckpt_folder is not None:
                utils.save_world(best_world, self.ckpt_folder+str(epoch)+".pkl")
                print("...saving epoch %d checkpoint. fitness: %.2f" % (epoch, best_world_fitness))

        return self.generation
    

    # one iteration
    def step(self):
        # We will calculate the fitness scores of each of the molds
        fitness_scores = []
        index = 0

        # We will loop through each of the worlds from the generation list
        for worlds in self.generation:
            # We will simulate the world
            worlds.simulate(steps=self.sim_steps)

            # We will then calculate the fitness score
            fitness = worlds.fitness()

            # We will then appeand a tuple that contains (fitness score, index of world)
            fitness_scores.append((fitness, index))

            # We then increment the index by 1
            index+=1
        
        # We will then sort the list of fitness scores in descending order
        fitness_scores.sort(reverse=True)
        #print(" > top fitness: %f" % fitness_scores[0][0])

        # Based on the success_ratio, we will take ~success_ration% of the world of molds to move on to the new iteration of the
        # Genetic Algorithm
        successors_size = int(self.generation_size*self.success_ratio)
        fitness_scores = fitness_scores[0:successors_size]

        #print(fitness_scores[0][0])

        # We will then create a list of parents
        parents = []

        # We will loop through the fitness scores
        for combo in fitness_scores:
            # We will take the generation world of mold at the given index(represented by combo[1])
            parents.append(self.generation[combo[1]])

        # We will reset the generation set
        self.generation = []

        # We will loop through the parents of the world
        for worlds in parents:
            # We will create a new world of molds
            new_world = self.world_function(fitness_function=self.fitness_function)

            # We will then loop through the chromosomes
            chromosomes = new_world.mold.chromosome.keys()
            for chromosome in chromosomes:
                # We will simply match the value of the chromosome to the current parent
                new_world.mold.chromosome[chromosome] = worlds.mold.chromosome[chromosome]
            
            # We will then append the parent freshly reset in the list of generations
            self.generation.append(new_world)

        # We will then repopulate the generation set until we have a size of 'generation_size'
        while len(self.generation) < self.generation_size:
            # We will compute index 1 and 2 that will represent parents 1 and 2
            index1 = random.randint(0, len(parents)-1)
            index2 = random.randint(0, len(parents)-1)

            # We will then perfor...hehehehehe
            self.sex(parents[index1], parents[index2])