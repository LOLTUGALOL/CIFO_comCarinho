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
        valid_set=[0,0],
    ):
        # Define a list of probabilities, where the first element will be the probability of having 0 in the representation, and the other
        # will be the probability of generating a random number between 0.1 and 1 (specified in the valid_set list, that is initialized in the sdp file.
        # Below you can see this implemented. We chose to have a valid_set between 0.1 and 1 because we didn't want to include the probability of
        # generating a zero twice.
        probabilities = [0.7, 0.3]

        # If our individual doesn't have a representation, we will generate one
        if representation == None:
            while True:
                self.representation = [round(random.choices([0, round(random.uniform(valid_set[0], valid_set[1]), 1)], probabilities)[0], 1) for _ in range(size)]
                # Then, we check if the created individual satisfies the macros, i.e. the minimum daily recommended intake of the nutrients specified in the
                # target_macros (in sdp_data).
                # We keep generating representations, until the macros are satisfied.
                if self.verify_macros()[0]:
                    break
        else:
            self.representation = representation
        self.fitness = self.get_fitness()

    # Define the fitness function, that will be the price of the diet plan.
    def get_fitness(self):
        price = 0

        # For every food (corresponds to every position in the representation), multiply its quantity, that is given by the factor, that is the element i of the
        # individual's representation, by the price of that food, and multiply it by 0.01, in order to get the price in dollars, since the price we are receiving is in cents.
        # Sum the values obtained for each food, in order to get the overall diet's price.
        for i, food in enumerate(foods.index):
            factor = self.representation[i]
            price += factor * foods.loc[food, 'price'] * 0.01

        return price

    # Define a function that verifies if the target_macros are being satisfied.
    def verify_macros(self):
        valid = True
        # Initialize a dictionary that will contain the names of the nutrients and associated to them the amounts of each one present in the diet plan
        nutrients = {}
        for i, food in enumerate(foods.index):
            factor = self.representation[i] # Corresponds to the amount of each food in one individual
            for nutrient in target_macros.keys():
                if nutrient not in nutrients: # If the nutrient isn't already in the dictionary, we add it and initialize its value to 0
                    nutrients[nutrient] = 0
                # If it already exists, we add to the value it already had the factor multiplied by the price by 0.01 by the amount of the nutrient.
                # By doing so, we are getting the price of the foods for the specified amounts in dollars (as we calculated in the verify_macros()), and then
                # we multiply it by the amount of nutrient, because the amounts of nutrients we have are corresponding to 1 dollar.
                nutrients[nutrient] += factor * foods.loc[food]['price'] * 0.01 * foods.loc[food][nutrient]

        # Now our nutrients dictionary contains the amounts of each nutrient for the current diet plan.
        for nutrient in nutrients.keys():
            # Finally, we do a if condition to check if the target_macros are being achieved
            if nutrients[nutrient] < target_macros[nutrient]:
                # If the amounts of nutrients we have are less than the target_macros, we return valid = False
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
        self.best_sol_macros = []
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    # replacement=kwargs["replacement"],
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

            return valid, nutrients

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

    def evolve(self, gens, replacement, select, crossover, mutate, xo_p, mut_p, elitism, fitness_sharing):
        self.best_sol_per_gen = []
        self.best_sol_macros = []
        for i in range(gens):
            new_pop = []

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
                if replacement == False:
                    while parent2 == parent1:
                        parent2 = select(self)

                parent1_ = deepcopy(parent1)
                parent2_ = deepcopy(parent2)

                counter = 0
                while True:
                    # XO
                    # 0.5 = probability of xo
                    if random.random() < xo_p and counter < 20:
                        offspring1, offspring2 = crossover(parent1, parent2)
                    else:
                        offspring1, offspring2 = parent1_, parent2_

                    if random.random() < mut_p and counter < 20:
                        offspring1 = mutate(offspring1)
                    if random.random() < mut_p and counter < 20:
                        offspring2 = mutate(offspring2)

                    if self.verify_macros(offspring1)[0] and self.verify_macros(offspring2)[0]:
                        break

                    counter += 1
                    if counter%5 == 0:
                        print(counter)

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
            self.best_sol_per_gen.append(self.best_sol.get_fitness())

        self.best_fitness = {min(self.best_sol_per_gen)}
        self.best_sol_macros = self.best_sol.verify_macros()[1]

    def get_best_representation(self):
        return self.best_sol.get_representation()

    def get_best_sol_per_gen(self):
        return self.best_sol_per_gen

    def get_best_sol(self):
        return self.best_sol

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
