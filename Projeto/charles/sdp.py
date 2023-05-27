import pandas as pd
from copy import deepcopy
from sdp_data import foods
from charles import Population
from selection import tournament, ranking, fps
from mutation import swap_mutation, inversion_mutation, gaussian_mutation
from crossover import arithmetic_co, single_point_co, multi_point_co
import itertools

def start(runs_data, test_name, selection, crossover, mutation, elitism, fitness_sharing):
    for run in range(10):
        pop_ = Population(size=100, optim="min", sol_size=len(foods), valid_set=[0.1, 1], replacement=True)
        pop_.evolve(gens=15, select=selection, crossover=crossover, mutate=mutation, xo_p=0.9, mut_p=0.2,
                    elitism=elitism, fitness_sharing=fitness_sharing)

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

    return runs_data


selections = ['tournament', 'ranking'] #'fps',
crossovers = ['arithmetic_co', 'single_point_co', 'multi_point_co']
mutations = ['swap_mutation', 'gaussian_mutation'] #'inversion_mutation',
elitisms = [True, False]
fitness_sharings = [True, False]

combinations = list(itertools.product(selections, crossovers, mutations, elitisms, fitness_sharings))

runs_data = {
    'Test': [],
    'Run': [],
    'Best_sol_per_gen': [],
    'Best_Fitness': [],
    'Best_Diet': []
}

for i, combination in enumerate(combinations):
    name = str(combinations[i])
    selection, crossover, mutation, elitism, fitness_sharing = combination
    print(selection, crossover, mutation, elitism, fitness_sharing)
    runs_data = start(runs_data, name, tournament, multi_point_co, swap_mutation, False, False)

df = pd.DataFrame(runs_data)

# Write the DataFrame to a single sheet
with pd.ExcelWriter('results_final.xlsx') as writer:
    sheet_name = 'Combined'  # Choose a name for the sheet
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Save the Excel file
    writer.save()