import random
from random import randint, uniform, choice, sample

def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2
'''
def arithmetic_co(p1,p2):

    offspring1= [None] * len(p1)
    offspring2= [None] * len(p1)

    #set a value for alpha bw 0-1

    alpha = uniform(0,1)

    # take the weighted sum of the parents according to the formula
    for i in range(len(p1)):
        offspring1[i] = p1[i] * alpha + (1 - alpha) * p2[i]
        offspring2[i] = p2[i] * alpha + (1 - alpha) * p1[i]
    return offspring1, offspring2
'''
def multi_point_co(p1, p2):

    num_co_points = randint(2, 5)
    co_points = sorted(sample(range(len(p1)), num_co_points))

    offspring1 = []
    offspring2 = []

    for i in range(num_co_points + 1):
        start = co_points[i-1] if i > 0 else 0
        end = co_points[i] if i < num_co_points else len(p1)

        if i % 2 == 0:
            offspring1.extend(p1[start:end])
            offspring2.extend(p2[start:end])
        else:
            offspring1.extend(p2[start:end])
            offspring2.extend(p1[start:end])

    return offspring1, offspring2

def uniform_co(p1, p2):
    offspring1 = []
    offspring2 = []
    for gene1, gene2 in zip(p1, p2):
        if random.random() < 0.5:
            offspring1.append(gene1)
            offspring2.append(gene2)
        else:
            offspring1.append(gene2)
            offspring2.append(gene1)

    return offspring1, offspring2