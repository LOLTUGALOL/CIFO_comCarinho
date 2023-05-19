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

tresh = 0.8

def create_target_ratio(target_macros, tresh):
    target_ratio = target_macros
    for key in target_macros:
        target_ratio[key] = target_macros[key] * tresh

    return target_ratio


target_ratio = create_target_ratio(target_macros,tresh)



def verify_macros(self, representation):
    valid = True
    nutrients = {}
    invalid_nutrient = None
    for i, food in enumerate(foods.index):
        factor = representation[i]
        for nutrient in target_macros.keys():
            if nutrient not in nutrients:
                nutrients[nutrient] = 0
            if nutrient == "Calories":
                factor = factor * 1000
            nutrients[nutrient] += factor * foods.loc[food, nutrient]

    for nutrient in nutrients.keys():
        if nutrients[nutrient] < target_macros[nutrient]:
            valid = False
            invalid_nutrient = nutrient
            break

    print("factor:", nutrients)

    return valid



def validate_ratio(target_macros,target_ratio,total_nutrients):
    valid = True
    for key in target_ratio:
        if abs(total_nutrients[key] - target_macros[key]) > target_ratio[key] :
            valid = False #or a penalization
            break
    return valid


def get_fitness(self):
    # Assuming `foods` is a Pandas DataFrame

    diet_plan = []
    price = 0
    return sum(self.representation)

    '''
    for i, food in enumerate(foods.index):
        factor = self.representation[i]
        price += factor * foods.loc[food, "price"]
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
    total_price = price

    total_nutrients = {
        "Calories": sum(item["nutrients"]["Calories"] for item in diet_plan),
        "Protein": sum(item["nutrients"]["Protein"] for item in diet_plan),
        "Calcium": sum(item["nutrients"]["Calcium"] for item in diet_plan),
        "Iron": sum(item["nutrients"]["Iron"] for item in diet_plan),
        "Vitamin A": sum(item["nutrients"]["Vitamin A"] for item in diet_plan),
        "Vitamin B1": sum(item["nutrients"]["Vitamin B1"] for item in diet_plan),
        "Vitamin B2": sum(item["nutrients"]["Vitamin B2"] for item in diet_plan),
        "Niacin": sum(item["nutrients"]["Niacin"] for item in diet_plan),
        "Vitamin C": sum(item["nutrients"]["Vitamin C"] for item in diet_plan)
    }



    if validate_ratio(target_macros,target_ratio,total_nutrients) :
        ratio = {
            'Calories': total_nutrients['Calories'] / target_macros['Calories'],
            'Protein': total_nutrients['Protein'] / target_macros['Protein'],
            'Calcium': total_nutrients['Calcium'] / target_macros['Calcium'],
            'Iron': total_nutrients['Iron'] / target_macros['Iron'],
            'Vitamin A': total_nutrients['Vitamin A'] / target_macros['Vitamin A'],
            'Vitamin B1': total_nutrients['Vitamin B1'] / target_macros['Vitamin B1'],
            'Vitamin B2': total_nutrients['Vitamin B2'] / target_macros['Vitamin B2'],
            'Niacin': total_nutrients['Niacin'] / target_macros['Niacin'],
            'Vitamin C': total_nutrients['Vitamin C'] / target_macros['Vitamin C'],
        }
        # Calculate the fitness based on the proximity of the ratio to the target ratio
        # We need to optimize two variables
        abs_dif = (abs(statistics.mean(ratio.values()) - 1))

        fitness = total_price
        return fitness, abs_dif, total_price
    else:
        fitness = 10000 # ou uma penalização
        abs_dif = 10000
        total_price = 10000
        return fitness, abs_dif, total_price

    # fit_price = total_price
    # fit_macros = abs(ratio_mean - 1)
    # return fit_price, fit_macros
'''

Individual.get_fitness = get_fitness
Individual.verify_macros = verify_macros

pop = Population(size=50, optim="min", sol_size=len(foods), valid_set=[0, 1], replacement=True)
pop.evolve(gens=30, select=tournament, crossover=aritmetic_xo, mutate=binary_mutation, xo_p=0.9, mut_p=0.2, elitism = True)

# Print the best solution
#print("price:", max(pop.individuals, key=attrgetter("fitness")).price)

#print("Best solution: ", best_solution)

# Print the price of the best solution
