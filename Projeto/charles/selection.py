import random
from operator import attrgetter
from random import choice, sample, choices

def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":

        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = random.uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        total_fitness = sum([1 / i.fitness for i in population]) # inverse because we want to give more chances to individuals with lower fitness values
        spin = random.uniform(0, total_fitness)
        position = 0
        for individual in population:
            position += 1 / individual.fitness
            if position > spin:
                return individual

    else:
        raise Exception("No optimization specified (min or max).")

def tournament(population, size=4):
    # Select randomly 4 individuals from the population
    tournament = sample(population.individuals, size)

    # From those individuals, return the one with the max/min fitness value, depending on the type of problem
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")

def ranking(population): # vai escolher um parent
    # Sort the population by fitness
    if population.optim == "max":
        sorted_population = sorted(population.individuals, key = attrgetter("fitness"), reverse =True)
    elif population.optim == "min":
        sorted_population = sorted(population.individuals, key = attrgetter("fitness"))
    else:
        raise Exception("No optimization specified (min or max).")

    # Calculate the sum of ranks from all individuals
    sum_ranks = sum(range(1, len(sorted_population) + 1))

    # Create a list that contains the probabilities of each individual being selected
    selection_probabilities = []
    for rank in range(1, len(sorted_population) + 1):
        selection_probabilities.append(rank / sum_ranks)

    # Select the individual to be returned based on the selection_probabilities
    selected_indiv = choices(sorted_population, selection_probabilities, k=1)[0]

    return selected_indiv


