import random
import copy
from copy import deepcopy
from operator import attrgetter
import sdp_data
from sdp_data import foods, target_macros
from mutation import swap_mutation

class Individual:
    def __init__(
        self,
        representation= None,
        size=None,
        replacement=True, # tends to produce a more diverse population
        valid_set=[0,0],
    ):
        # options = [0, random.uniform(valid_set[0], valid_set[1])]
        probabilities = [0.7, 0.3]

        c = 0
        if representation == None:
            while True:

                if replacement == True:
                    #self.representation = random.choices([0, random.uniform(valid_set[0], valid_set[1])], probabilities, k = size)
                    #self.representation = [random.choices([0, random.uniform(valid_set[0], valid_set[1])], probabilities)[0] for _ in range(size)]
                    self.representation = [round(random.choices([0, round(random.uniform(valid_set[0], valid_set[1]), 1)],
                                          probabilities)[0], 1) for _ in range(size)]
                elif replacement == False:
                    self.representation = round(round(random.sample(random.uniform(valid_set[0],valid_set[1]), size), 1), 1)
                print('representation: ',self.representation)
                if self.verify_macros():
                    break

                print('tentativa: ',c)
                c += 1
        else:
            self.representation = representation

        self.fitness = self.get_fitness()
        #self.abs_dif = self.get_fitness()[1]
        #self.price = self.get_fitness()[

    def get_fitness(self):
        price = 0

        for i, food in enumerate(foods.index):
            factor = self.representation[i]
            price += factor * foods.loc[food, 'price'] * 0.01
        print('price: ', price)
        return price
        # raise Exception("You need to monkey patch the fitness path.")
    def verify_macros(self):
            valid = True
            nutrients = {}
            invalid_nutrient = None
            for i, food in enumerate(foods.index):
                factor = self.representation[i]
                for nutrient in target_macros.keys():
                    if nutrient not in nutrients:
                        nutrients[nutrient] = 0
                    #if nutrient == "Calories":
                     #   factor = factor * 100
                    nutrients[nutrient] += factor * foods.loc[food]['price'] * 0.01 * foods.loc[food][nutrient]

            for nutrient in nutrients.keys():
                if nutrients[nutrient] < target_macros[nutrient]:
                    valid = False
                    invalid_nutrient = nutrient
                    break

            print("Nutrients:", nutrients)

            return valid
        # raise Exception("invalid indiv")

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
        self.best_sol = None
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    replacement=kwargs["replacement"],
                    valid_set=kwargs["valid_set"],
                )
            )
            self.individuals[_].__repr__

    def verify_macros(self, representation):
            valid = True
            nutrients = {}
            invalid_nutrient = None
            for i, food in enumerate(foods.index):
                factor = representation[i]
                for nutrient in target_macros.keys():
                    if nutrient not in nutrients:
                        nutrients[nutrient] = 0
                    nutrients[nutrient] += factor * foods.loc[food]['price'] * 0.01 * foods.loc[food][nutrient]

            for nutrient in nutrients.keys():
                if nutrients[nutrient] < target_macros[nutrient]:
                    valid = False
                    invalid_nutrient = nutrient
                    break

            print("Nutrients offspring:", nutrients)

            return valid

    def evolve(self, gens, select, crossover, mutate, xo_p, mut_p, elitism):
        for i in range(gens):
            new_pop = []

            if elitism:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key = attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key= attrgetter("fitness")))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)

                while True:
                    # XO
                    # 0.5 = probability of xo
                    if random.random() < xo_p:
                        offspring1, offspring2 = crossover(parent1, parent2)
                    else:
                        offspring1, offspring2 = parent1, parent2

                    if random.random() < mut_p:
                        offspring1 = mutate(offspring1)
                    if random.random() < mut_p:
                        offspring2 = mutate(offspring2)

                    if self.verify_macros(offspring1) and self.verify_macros(offspring2):
                        break

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                if self.optim == "max":
                    worst = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == "min":
                    worst = max(new_pop, key=attrgetter("fitness"))

                new_pop.pop(new_pop.index(worst))
                new_pop.append(elite)

            self.individuals = new_pop
            self.best_sol = {min(new_pop, key=attrgetter("fitness"))}
            print(f'Best individual: { self.best_sol }')

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
