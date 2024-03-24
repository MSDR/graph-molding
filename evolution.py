import world
import random

class GeneticAlgorithm():
    def __init__(self, epochs, mutation_rate, generation_size, success_ratio):
        # number of full simulations to run
        self.epochs = epochs

        # rate of mutation per gene btw [0,1]
        self.mutation_rate = mutation_rate

        # number of molds per generation
        self.generation_size = generation_size

        # percent of top performing parents for next generation
        self.success_ratio = success_ratio

        # list of worlds, each with their own single mold
        self.generation = self.first_generation(generation_size)


    # populates first generation of worlds
    def first_generation(self, generation_size):
        generational_molds = []

        for generation in range(generation_size):
            new_world = world.World()
            chromosomes = new_world.mold.chromosome.keys()
            for chromosome in chromosomes:
                new_world.mold.chromosome[chromosome] = random.random()

            generational_molds.append(new_world)

        return generational_molds
        #pass

    def sex(self, parent1, parent2):
        new_world = world.World()
        chromosomes = new_world.mold.chromosome.keys()
        for chromosome in chromosomes:
            if random.random() < self.mutation_rate:
                new_world.mold.chromosome[chromosome] = random.random()
            else:
                if random.randint(0, 1) == 0:
                    new_world.mold.chromosome[chromosome] = parent1.mold.chromosome[chromosome]
                else:
                    new_world.mold.chromosome[chromosome] = parent2.mold.chromosome[chromosome]
        self.generation.append(new_world)

    def run_algorithm(self):
        for epoch in range(self.epochs):
            print(epoch)
            self.step()
        return self.generation

    # one iteration
    def step(self):
        fitness_scores = []
        index = 0
        for worlds in self.generation:
            worlds.simulate()
            fitness = worlds.mold.fitness()
            fitness_scores.append((fitness, index))
            index+=1
        
        fitness_scores.sort(reverse=True)

        successors_size = int(self.generation_size*self.success_ratio)
        fitness_scores = fitness_scores[0:successors_size]

        print(fitness_scores[0][0])

        parents = []
        for combo in fitness_scores:
            parents.append(self.generation[combo[1]])

        self.generation = []

        for worlds in parents:
            new_world = world.World()
            chromosomes = new_world.mold.chromosome.keys()
            for chromosome in chromosomes:
                new_world.mold.chromosome[chromosome] = worlds.mold.chromosome[chromosome]
            self.generation.append(new_world)


        while len(self.generation) < self.generation_size:
            index1 = random.randint(0, len(parents)-1)
            index2 = random.randint(0, len(parents)-1)
            self.sex(parents[index1], parents[index2])

GA = GeneticAlgorithm(50, 0.01, 10, 0.1)

worlds = GA.run_algorithm()

W = worlds[0]
W.simulate(steps=30, display=True)

chromosomes = W.mold.chromosome.keys()
for chromosome in chromosomes:
    print("%s: %f" %(chromosome, W.mold.chromosome[chromosome]))
