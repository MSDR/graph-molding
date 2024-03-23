import world

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
        self.generation = self.first_generation()

    # populates first generation of worlds
    def first_generation(self, generation_size):
        pass

    def sex(self, parent1, parent2):
        pass

    def run_algorithm(self):
        pass

    # one iteration
    def step(self):
        # for world in generation:
        #   world.simulate()
        #   fitness = world.mold.fitness()
        pass


