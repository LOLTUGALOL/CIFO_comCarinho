import pandas as pd
from copy import deepcopy
from sdp_data import foods
from charles import Population
from selection import tournament, ranking, fps
from mutation import swap_mutation, inversion_mutation, random_mutation
from crossover import uniform_co, single_point_co, multi_point_co
import itertools
'''
pop_ = Population(size=10, optim="min", sol_size=len(foods), valid_set=[0, 1])
pop_.evolve(gens=5, replacement=False, select=tournament, crossover=multi_point_co, mutate=random_mutation, xo_p=0.9, mut_p=0.2, elitism = True, fitness_sharing = False)

final_representation = deepcopy(pop_.get_best_representation())

diet_plan = {}

for i, q, u in zip(foods.index.tolist(), foods['quantity'].tolist(), foods['unit'].tolist()):
    value = f"{final_representation.pop(0) * q} {u}"
    diet_plan[i] = value
print('Final Diet Plan: ', diet_plan)

filtered_diet_plan = {key: value for key, value in diet_plan.items() if not value.startswith('0.0')}
print('Final Filtered Diet Plan', filtered_diet_plan)
print(len(filtered_diet_plan))
'''

def start(runs_data, test_name, selection, crossover, mutation, elitism, fitness_sharing):
    for run in range(5):
        pop_ = Population(size=80, optim="min", sol_size=len(foods), valid_set=[0.1, 1])
        pop_.evolve(gens=30, replacement=False, select=selection, crossover=crossover, mutate=mutation, xo_p=0.9, mut_p=0.2, elitism=elitism, fitness_sharing=fitness_sharing)

        final_representation = deepcopy(pop_.get_best_representation())

        diet_plan = {}

        for i, q, u in zip(foods.index.tolist(), foods['quantity'].tolist(), foods['unit'].tolist()):
            value = f"{final_representation.pop(0) * q} {u}"
            diet_plan[i] = value
        print('Final Diet Plan:', diet_plan)

        filtered_diet_plan = {key: value for key, value in diet_plan.items() if not value.startswith('0.0')}
        print('Final Filtered Diet Plan:', filtered_diet_plan)

        run_number = run + 1
        test_column_value = test_name if run_number == 1 else ''
        runs_data['Test'].append(test_column_value)
        runs_data['Run'].append(run_number)
        runs_data['Best_sol_per_gen'].append(pop_.get_best_sol_per_gen())
        runs_data['Best_Fitness'].append(pop_.best_fitness)
        runs_data['Best_Diet'].append(filtered_diet_plan)
        runs_data['Macros'].append(pop_.best_sol_macros)

    return runs_data


selections = [fps]#, tournament, ranking]
crossovers = [single_point_co, multi_point_co, uniform_co]
mutations = [swap_mutation, inversion_mutation, random_mutation]
elitisms = [False, True]
fitness_sharings = [False, True]

selections_str = ['fps']#, 'tournament', 'ranking']
crossovers_str = ['single_point_co', 'multi_point_co', 'uniform_co']
mutations_str = ['swap_mutation', 'inversion_mutation', 'random_mutation']
elitisms_ = [False, True]
fitness_sharings_ = [False, True]

combinations = list(itertools.product(selections, crossovers, mutations, elitisms, fitness_sharings))
combinations_str = list(itertools.product(selections_str, crossovers_str, mutations_str, elitisms_, fitness_sharings_))


runs_data = {
    'Test': [],
    'Run': [],
    'Best_sol_per_gen': [],
    'Best_Fitness': [],
    'Best_Diet': [],
    'Macros': []
}

for i, combination in enumerate(combinations):
    name = str(combinations_str[i])
    selection, crossover, mutation, elitism, fitness_sharing = combination
    print('---> ', name)
    runs_data = start(runs_data, name, selection, crossover, mutation, elitism, fitness_sharing)

df = pd.DataFrame(runs_data)

# Write the DataFrame to a single sheet
with pd.ExcelWriter('results_final.xlsx') as writer:
    sheet_name = 'Combined'  # Choose a name for the sheet
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Save the Excel file
    writer.save()
