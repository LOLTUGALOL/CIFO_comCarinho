from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from copy import deepcopy
from charles.selection import tournament, tournament_selection, get_non_dominated_tournament, dominates
from charles.mutation import binary_mutation
from charles.crossover import aritmetic_xo
from random import random
from operator import attrgetter
from sdp_data import foods, target_macros
import statistics
import pandas as pd

def get_fitness(self):
    # Assuming `foods` is a Pandas DataFrame

    diet_plan = []

    for i, food in enumerate(foods.index):
        factor = self.representation[i]
        price = factor * foods.loc[food, "price"]
        quantity = factor * foods.loc[food, "quantity"]

        nutrients = {
            'Calories': factor * foods.loc[food, 'Calories'],
            'Protein': factor * foods.loc[food, 'Protein'],
            'Calcium': factor * foods.loc[food, 'Calcium'],
            'Iron': factor * foods.loc[food, 'Iron'],
            'Vitamin A': factor * foods.loc[food, 'Vitamin A'],
            'Vitamin B1': factor * foods.loc[food, 'Vitamin B1'],
            'Vitamin B2': factor * foods.loc[food, 'Vitamin B2'],
            'Niacin': factor * foods.loc[food, 'Niacin'],
            'Vitamin C': factor * foods.loc[food, 'Vitamin C']
        }

        diet_plan.append({"food": food, "price": price, "nutrients": nutrients})

    # Calculate the price and macronutrient ratio of the diet plan
    total_price =  sum(item["price"] for item in diet_plan)

    total_calories = sum(item["nutrients"]["Calories"] for item in diet_plan)
    total_protein = sum(item["nutrients"]["Protein"] for item in diet_plan)
    total_calcium = sum(item["nutrients"]["Calcium"] for item in diet_plan)
    total_iron = sum(item["nutrients"]["Iron"] for item in diet_plan)
    total_VA = sum(item["nutrients"]["Vitamin A"] for item in diet_plan)
    total_VB1 = sum(item["nutrients"]["Vitamin B1"] for item in diet_plan)
    total_VB2 = sum(item["nutrients"]["Vitamin B2"] for item in diet_plan)
    total_Niacin = sum(item["nutrients"]["Niacin"] for item in diet_plan)
    total_VC = sum(item["nutrients"]["Vitamin C"] for item in diet_plan)

    ratio = {
        'Calories': total_calories/target_macros['Calories'],
        'Protein': total_protein/target_macros['Protein'],
        'Calcium': total_calcium/target_macros['Calcium'],
        'Iron': total_iron/target_macros['Iron'],
        'Vitamin A': total_VA/target_macros['Vitamin A'],
        'Vitamin B1': total_VB1/target_macros['Vitamin B1'],
        'Vitamin B2': total_VB2/target_macros['Vitamin B2'],
        'Niacin': total_Niacin/target_macros['Niacin'],
        'Vitamin C': total_VC/target_macros['Vitamin C'],
    }
    # Calculate the fitness based on the proximity of the ratio to the target ratio
    # We need to optimize two variables
    ratio_mean = statistics.mean(ratio.values())

    fitness = 0.2 * total_price + 0.8 * (abs(ratio_mean - 1) * 10)

    return fitness

    # fit_price = total_price
    # fit_macros = abs(ratio_mean - 1)
    # return fit_price, fit_macros


Individual.get_fitness = get_fitness

pop = Population(size=50, optim="min", sol_size=len(foods), valid_set=[0, 3], replacement=True)
pop.evolve(gens=30, select=tournament, crossover=aritmetic_xo, mutate=binary_mutation, xo_p=0.9, mut_p=0.2, elitism = True)

# Print the best solution
best_solution = hof[0]
print("Best solution: ", best_solution)

# Print the price of the best solution
best_price = best_solution.fitness.values[0]
print("Price of the best solution: ", best_price)