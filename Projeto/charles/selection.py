import random
from operator import attrgetter
from random import choice, sample

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
        raise NotImplementedError

    else:
        raise Exception("No optimization specified (min or max).")

def tournament(population, size=4):
    tournament = sample(population.individuals, size)

    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))
'''
def ranking():
    # Rank Based Selection
    def rank_based_selection(population, num_parents):
        # Sort the population by fitness in descending order
        sorted_population = sorted(population, key=lambda x: attrgetter("fitness"), reverse=True)

        # Calculate the selection probabilities using the rank-based approach
        num_individuals = len(sorted_population)
        selection_probabilities = [
            ((2 - alpha) / num_individuals) + ((2 * i * (alpha - 1)) / (num_individuals * (num_individuals - 1))) for i
            in range(num_individuals)]

        # Select the parents based on their rank and the selection probabilities
        selected_parents_indices = choice(num_individuals, size=num_parents, replace=False,
                                                    p=selection_probabilities)
        selected_parents = [sorted_population[i] for i in selected_parents_indices]

        return selected_parents
'''

def linear_ranking_selection(population, max_prob=1.0, min_prob=0.0):
    pop_size = len(population)
    ranks = list(range(1, pop_size + 1))
    total_ranks = sum(ranks)
    selection_probs = [(max_prob - ((max_prob - min_prob) * (rank - 1) / (pop_size - 1))) for rank in ranks]
    selected = []

    for _ in range(pop_size):
        selected_index = roulette_wheel_selection(selection_probs)
        selected.append(population[selected_index])

    return selected

def roulette_wheel_selection(selection_probs):
    total_probs = sum(selection_probs)
    rand_num = random.uniform(0, total_probs)
    partial_sum = 0

    for i, prob in enumerate(selection_probs):
        partial_sum += prob
        if partial_sum >= rand_num:
            return i

    return len(selection_probs) - 1
