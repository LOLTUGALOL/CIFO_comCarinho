from random import randint, uniform, choice

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

def aritmetic_xo(p1,p2):

    offspring1= [None] * len(p1)
    offspring2= [None] * len(p1)

    #set a value for alpha bw 0-1

    alpha = uniform(0,1)

    # take the weighted sum of the parents according to the formula
    for i in range(len(p1)):
        offspring1[i] = p1[i] * alpha + (1-alpha) * p2[i]
        offspring2[i] = p2[i] * alpha + (1 - alpha) * p1[i]

    return offspring1, offspring2

# Heuristic Crossover
