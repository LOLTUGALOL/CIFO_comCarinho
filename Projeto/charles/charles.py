import random
import copy
from operator import attrgetter
# from charles.mutation import binary_mutation

class Individual:
    def __init__(
        self,
        representation=None,
        size=None,
        replacement=True, # tends to produce a more diverse population
        valid_set=[0, 3],
    ):
        options = [0,random.uniform(valid_set[0], valid_set[1])]
        probabilities = [0.5, 0.5]

        if representation == None:
            if replacement == True:
                self.representation = random.choices(options, probabilities, k = size)
            elif replacement == False:
                self.representation = sample(random.uniform(valid_set[0],valid_set[1]), size)
        else:
            self.representation = representation
        self.fitness = self.get_fitness()

    def get_fitness(self):

        raise Exception("You need to monkey patch the fitness path.")

    def get_neighbours(self, func, **kwargs):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"


class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    replacement=kwargs["replacement"],
                    valid_set=kwargs["valid_set"],
                )
            )


    def evolve(self, gens, select, crossover, mutate, xo_p, mut_p, elitism):

        for i in range(gens):
            new_pop = []

            if elitism:
                if self.optim == "max":
                    elite = copy.deepcopy(max(self.individuals, key = attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(max(self.individuals, key= attregetter("fitness")))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)

                # XO
                # 0.5 = probability of xo
                if random.random() < xo_p:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                if random.random() < mut_p:
                    offspring1 = mutate(offspring1)
                if random.random() < mut_p:
                    offspring2 = binary_mutation(offspring2)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                if self.optim == "max":
                    worst = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == "min":
                    worst = max(new_pop, key=attrgetter("fitness"))

                new_pop.pop(new_pop.index(worst))


            self.individuals = new_pop
            print(f'Best individual: { max(new_pop, key=attrgetter("fitness"))}')

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
