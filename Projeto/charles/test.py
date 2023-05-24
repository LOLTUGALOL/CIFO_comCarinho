import random
from random import choices

sorted_population = [5, 3, 2, 4, 1]

sum_ranks = sum(range(1, len(sorted_population) + 1))

selection_probabilities = []
for rank in range(1, len(sorted_population) + 1):
    selection_probabilities.append(rank / sum_ranks)

selected_indiv = choices(sorted_population, selection_probabilities, k=1)[0]

print(selected_indiv)