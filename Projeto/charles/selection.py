import random
from operator import attrgetter
from random import choice, sample

# tournament selection with NSGA-II
def dominates(fitness_values1, fitness_values2):
    """
    Check if fitness_values1 dominates fitness_values2
    """
    for i in range(len(fitness_values1)):
        if fitness_values1[i] > fitness_values2[i]:
            return False
    return True

def get_non_dominated_tournament(tournament):
    non_dominated_tournament = []
    for i in range(len(tournament)):
        is_dominated = False
        for j in range(len(tournament)):
            if i != j and dominates(tournament[j].get_fitness(), tournament[i].get_fitness()):
                is_dominated = True
                break
        if not is_dominated:
            non_dominated_tournament.append(tournament[i])
    return non_dominated_tournament

def tournament_selection(population, tournament_size = 4):
    selected_parents = []
    for i in range(len(population)):
        tournament = random.sample(population.individuals, tournament_size)
        non_dominated_tournament = get_non_dominated_tournament(tournament)
        selected_parents.append(random.choice(non_dominated_tournament))
    return selected_parents


def get_crowding_distance(individuals):
    """
    Calculate the crowding distance for a set of individuals
    """
    n_objectives = len(individuals[0].get_fitness())

    crowding_distances = [0.0] * len(individuals)

    for objective_index in range(n_objectives):
        sorted_individuals = sorted(individuals, key=lambda x: x.get_fitness()[objective_index])

        crowding_distances[0] = crowding_distances[-1] = float('inf')

        for i in range(1, len(individuals) - 1):
            crowding_distances[i] += (sorted_individuals[i + 1].get_fitness()[objective_index] -
                                      sorted_individuals[i - 1].get_fitness()[objective_index])

    return crowding_distances

def get_ranked_population(population):
    """
    Rank individuals in the population based on their non-dominated set and crowding distance
    """
    population_ranked = []

    # Get the non-dominated fronts
    fronts = get_non_dominated_fronts(population)

    for i, front in enumerate(fronts):
        # Set the rank of the individuals in this front
        for individual in front:
            individual.set_rank(i)

        # Calculate the crowding distance of the individuals in this front
        crowding_distances = get_crowding_distance(front)

        # Set the crowding distance of the individuals in this front
        for j, individual in enumerate(front):
            individual.set_crowding_distance(crowding_distances[j])

        population_ranked.extend(front)

    return population_ranked

def tournament_selection(population, tournament_size = 4):
    selected_parents = []
    population_ranked = get_ranked_population(population)
    for i in range(len(population)):
        tournament = random.sample(population_ranked, tournament_size)
        non_dominated_tournament = get_non_dominated_tournament(tournament)
        non_dominated_tournament_sorted = sorted(non_dominated_tournament, key=lambda x: (x.get_rank(), -x.get_crowding_distance()))
        selected_parents.append(non_dominated_tournament_sorted[0])
    return selected_parents


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
    tournament[0]
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))



