import random
from copy import deepcopy
from operator import attrgetter
from sdp_data import foods, target_macros
import math

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

        if representation == None:
            while True:
                if replacement == True:
                    self.representation = [round(random.choices([0, round(random.uniform(valid_set[0], valid_set[1]), 1)],
                                          probabilities)[0], 1) for _ in range(size)]
                elif replacement == False:
                    self.representation = round(round(random.sample(random.uniform(valid_set[0],valid_set[1]), size), 1), 1)
                if self.verify_macros()[0]:
                    break
        else:
            self.representation = representation
        self.fitness = self.get_fitness()

    def get_fitness(self):
        price = 0

        for i, food in enumerate(foods.index):
            factor = self.representation[i]
            price += factor * foods.loc[food, 'price'] * 0.01

        return price

    #def return_fitness(self):
        #return self.fitness

    def verify_macros(self):
        valid = True
        nutrients = {}
        for i, food in enumerate(foods.index):
            factor = self.representation[i]
            for nutrient in target_macros.keys():
                if nutrient not in nutrients:
                    nutrients[nutrient] = 0
                nutrients[nutrient] += factor * foods.loc[food]['price'] * 0.01 * foods.loc[food][nutrient]

        for nutrient in nutrients.keys():
            if nutrients[nutrient] < target_macros[nutrient]:
                valid = False
                break

        # print("Nutrients:", nutrients)

        return valid, nutrients

    def get_representation(self):
        return self.representation

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}; Representation: {self.representation}"

class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.best_sol = None
        self.best_sol_per_gen = []
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    replacement=kwargs["replacement"],
                    valid_set=kwargs["valid_set"],
                )
            )

    def verify_macros(self, representation):
            valid = True
            nutrients = {}
            for i, food in enumerate(foods.index):
                factor = representation[i]
                for nutrient in target_macros.keys():
                    if nutrient not in nutrients:
                        nutrients[nutrient] = 0
                    nutrients[nutrient] += factor * foods.loc[food]['price'] * 0.01 * foods.loc[food][nutrient]

            for nutrient in nutrients.keys():
                if nutrients[nutrient] < target_macros[nutrient]:
                    valid = False
                    break

            # print("Nutrients offspring:", nutrients)

            return valid

    def euclidean_distance(self, individual1, individual2):
        if len(individual1) != len(individual2):
            raise ValueError("The two solutions must have the same length.")

        squared_diff_sum = sum((a - b) ** 2 for a, b in zip(individual1, individual2))
        distance = math.sqrt(squared_diff_sum)

        return distance

    def normalize_distances(self, distances):
        max_distance = max(distances)
        min_distance = min(distances)

        # If the max_distance is the same as the min_distance, the sharing coefficient would become infinite, meaning that all individuals are considered
        # part of the same niche. If that happens, we will consider to skip applying the Fitness Sharing method. Therefore, giving normalized_distances
        # the value of 1, the sharing coefficient will be also 1 (we defined it), which will not affect the fitness of the individual in question.
        if max_distance == min_distance:
            normalized_distances = 1
        else:
            normalized_distances = [(d - min_distance) / (max_distance - min_distance) for d in distances]
        return normalized_distances

    def evolve(self, gens, select, crossover, mutate, xo_p, mut_p, elitism, fitness_sharing):
        for i in range(gens):
            new_pop = []
            self.best_sol_per_gen = []

            if elitism:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key = attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key= attrgetter("fitness")))

            ### Fitness Sharing

            if fitness_sharing:
                # Adjust fitness values using fitness sharing

                for i in self.individuals:
                    sharing_sum = 0.0
                    distances = []

                    # Calculate the Euclidean distance between all individuals and save it in the distances list
                    for j in self.individuals:
                        if i != j:
                            distance = self.euclidean_distance(i, j)
                            distances.append(distance)

                    # Normalize the distances between 0 and 1
                    normalized_distances = self.normalize_distances(distances)

                    # Calculate the Sharing Coefficient, that is the sum of all the distances normalized
                    if normalized_distances == 1:
                        sharing_coefficient = 1
                    else:
                        sharing_coefficient = sum(normalized_distances)

                    i.fitness = i.fitness / sharing_coefficient

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

                if isinstance(offspring1, list):
                    new_pop.append(Individual(representation=offspring1))
                else:
                    new_pop.append(offspring1)

                if len(new_pop) < self.size:
                    if isinstance(offspring2, list):
                        new_pop.append(Individual(representation=offspring2))
                    else:
                        new_pop.append(offspring2)

            if elitism:
                if self.optim == "max":
                    worst = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == "min":
                    worst = max(new_pop, key=attrgetter("fitness"))

                new_pop.pop(new_pop.index(worst))
                new_pop.append(elite)

            self.individuals = new_pop
            self.best_sol = {min(self.individuals, key=attrgetter("fitness"))}
            print(f'Best individual: { self.best_sol }')

        self.best_sol = self.best_sol.pop()
        self.best_sol_per_gen.append(self.best_sol)

    def get_best_representation(self):
        return self.best_sol.get_representation()

    def get_best_sol_per_gen(self):
        return self.best_sol_per_gen

    def get_best_sol(self):
        return self.best_sol

    def get_best_fitness(self):
        return self.best_sol.get_fitness()

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
