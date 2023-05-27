from random import random
from operator import attrgetter
import statistics
import pandas as pd
from copy import deepcopy
from sdp_data import foods, target_macros
from charles import Population, Individual
from selection import tournament, ranking, fps
from mutation import swap_mutation, inversion_mutation, gaussian_mutation
from crossover import arithmetic_co, single_point_co, multi_point_co

def start(sheetname, selection, crossover, mutation,writer):
    runs_data = {
        'Run': [],
        # 'Best_Sol': [],
        # 'Best_Diet': [],
        # 'Best_sol_per_gen': [],
        'Best_Fitness': []
    }
    for run in range(3):
        pop_ = Population(size=10, optim="min", sol_size=len(foods), valid_set=[0, 1], replacement=True)
        pop_.evolve(gens=3, select=fps, crossover=multi_point_co, mutate=gaussian_mutation, xo_p=0.9, mut_p=0.2, elitism=True, fitness_sharing=True)

        final_representation = deepcopy(pop_.get_best_representation())

        diet_plan = {}

        for i, q, u in zip(foods.index.tolist(), foods['quantity'].tolist(), foods['unit'].tolist()):
            value = f"{final_representation.pop(0) * q} {u}"
            diet_plan[i] = value
        print('Final Diet Plan: ', diet_plan)

        filtered_diet_plan = {key: value for key, value in diet_plan.items() if not value.startswith('0.0')}
        print('Final Filtered Diet Plan', filtered_diet_plan)

        # pop_.get_best_sol().verify_macros()

        run_number = run + 1
        runs_data['Run'].append(run_number)
        # runs_data['Best_Sol'].append(pop_.get_best_sol())
        # runs_data['Best_Diet'].append(filtered_diet_plan)
        # runs_data['Best_sol_per_gen'].append(pop_.get_best_sol_per_gen())
        runs_data['Best_Fitness'].append(pop_.get_best_fitness())

        df = pd.DataFrame(runs_data)

        # Write the DataFrame to sheet
        sheet_name = sheetname
        df.to_excel(writer, sheet_name=sheet_name, index=False)


with pd.ExcelWriter('results_final.xlsx') as writer:
    # Call start function for each configuration
    start('Test1', ranking, arithmetic_co, swap_mutation, writer)
    start('Test2', tournament, single_point_co, inversion_mutation, writer)

    # Save the Excel file
    writer.save()
