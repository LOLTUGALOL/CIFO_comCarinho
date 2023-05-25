import random
from random import randint, sample, gauss

def swap_mutation(individual):
    """Swap mutation for a GA individual. Swaps the bits.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    individual[mut_indexes[0]], individual[mut_indexes[1]] = individual[mut_indexes[1]], individual[mut_indexes[0]]
    return individual


def inversion_mutation(individual):
    """Inversion mutation for a GA individual. Reverts a portion of the representation.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    mut_indexes.sort()
    individual[mut_indexes[0]:mut_indexes[1]] = individual[mut_indexes[0]:mut_indexes[1]][::-1]
    return individual

def gaussian_mutation(individual, mean=1.5, std_dev=1.5, mutation_rate=0.1):
    for i in range(len(individual)):
        if random() < mutation_rate:  # Check if mutation should occur
            # Generate a random index to mutate
            mutation_index = randint(0, len(individual) - 1)

            individual[mutation_index] += gauss(mean, std_dev)  # Apply Gaussian mutation to the gene

    return individual
