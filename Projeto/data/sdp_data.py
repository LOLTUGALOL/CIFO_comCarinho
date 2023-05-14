import random
import pandas as pd


# Define a dictionary of foods with their nutrient composition and recommended serving size
foods_index = {'Wheat Flour (Enriched)': 0,
              'Macaroni': 1,
              'Wheat Cereal (Enriched)': 2,
              'Corn Flakes': 3,
              'Corn Meal': 4,
              'Hominy Grits': 5,
              'Rice': 6,
              'Rolled Oats': 7,
              'White Bread (Enriched)': 8,
              'Whole Wheat Bread': 9,
              'Rye Bread': 10,
              'Pound Cake': 11,
              'Soda Crackers': 12,
              'Milk': 13,
              'Evaporated Milk (can)': 14,
              'Butter': 15,
              'Oleomargarine': 16,
              'Eggs': 17,
              'Cheese (Cheddar)': 18,
              'Cream': 19,
              'Peanut Butter': 20,
              'Mayonnaise': 21,
              'Crisco': 22,
              'Lard': 23,
              'Sirloin Steak': 24,
              'Round Steak': 25,
              'Rib Roast': 26,
              'Chuck Roast': 27,
              'Plate': 28,
              'Liver (Beef)': 29,
              'Leg of Lamb': 30,
              'Lamb Chops (Rib)': 31,
              'Pork Chops': 32,
              'Pork Loin Roast': 33,
              'Bacon': 34,
              'Ham, smoked': 35,
              'Salt Pork': 36,
              'Roasting Chicken': 37,
              'Veal Cutlets': 38,
              'Salmon, Pink (can)': 39,
              'Apples': 40,
              'Bananas': 41,
              'Lemons': 42,
              'Oranges': 43,
              'Green Beans': 44,
              'Cabbage': 45,
              'Carrots': 46,
              'Celery': 47,
              'Lettuce': 48,
              'Onions': 49,
              'Potatoes': 50,
              'Spinach': 51,
              'Sweet Potatoes': 52,
              'Peaches (can)': 53,
              'Pears (can)': 54,
              'Pineapple (can)': 55,
              'Asparagus (can)': 56,
              'Green Beans (can)': 57,
              'Pork and Beans (can)': 58,
              'Corn (can)': 59,
              'Peas (can)': 60,
              'Tomatoes (can)': 61,
              'Tomato Soup (can)': 62,
              'Peaches, Dried': 63,
              'Prunes, Dried': 64,
              'Raisins, Dried': 65,
              'Peas, Dried': 66,
              'Lima Beans, Dried': 67,
              'Navy Beans, Dried': 68,
              'Coffee': 69,
              'Tea': 70,
              'Cocoa': 71,
              'Chocolate': 72,
              'Sugar': 73,
              'Corn Syrup': 74,
              'Molasses': 75,
              'Strawberry Preserves':76
              }

nutrient_index = {'Calories (kcal)': 3,
                    'Protein (g)': 4,
                    'Calcium (g)': 5,
                    'Iron (mg)': 6,
                    'Vitamin A (KIU)': 7,
                    'Vitamin B1 (mg)': 8,
                    'Vitamin B2 (mg)': 9,
                    'Niacin (mg)': 10,
                    'Vitamin C (mg)':11
                    }

nutrient_index = {'Unit':'lb',
                  'Weight':3,
                  'Calories': 3,
                  'Protein': 4,
                'Calcium': 5,
                'Iron': 6,
                'Vitamin A': 7,
                'Vitamin B1': 8,
                'Vitamin B2': 9,
                'Niacin': 10,
                'Vitamin C':11,
                'Price': 10,
                    }


old_foods = {
        'Wheat Flour (Enriched)': {'unit': 'lb.', 'quantity': 10, 'price': 36, 'Calories': 44.7, 'Protein': 1411, 'Calcium': 2, 'Iron': 365, 'Vitamin A': 0,
                                   'Vitamin B1': 55.4, 'Vitamin B2': 33.3, 'Niacin': 441, 'Vitamin C': 0 },
        'Macaroni': {'unit': 'lb.', 'quantity': 1, 'price': 14.1, 'Calories': 11.6, 'Protein': 418, 'Calcium': 0.7, 'Iron': 54, 'Vitamin A': 0,
                                   'Vitamin B1': 3.2, 'Vitamin B2': 1.9, 'Niacin': 68, 'Vitamin C': 0 },
        'Wheat Cereal (Enriched)': {'unit': 'oz.', 'quantity': 28, 'price': 24.2, 'Calories': 11.8, 'Protein': 377, 'Calcium': 14.4, 'Iron': 175, 'Vitamin A': 0,
                                   'Vitamin B1': 14.4, 'Vitamin B2': 8.8, 'Niacin': 114, 'Vitamin C': 0 },
}

foods = pd.read_excel(r"/GitHub/CIFO_comCarinho/Projeto/SDP_data.xlsx")
foods.set_index("Commodity", inplace = True)

# Define the number of genes (scaling factors)
num_genes = len(foods)

[0,3]

[0.2,0,1,0,1,1,1]

# Define the range of possible values for each gene (scaling factor)
gene_range = (0.5, 1.5)

# Define the target macronutrient ratio
target_macros = {
            'Calories': 3000,
            'Protein': 70,
            'Calcium': 0.8,
            'Iron': 12,
            'Vitamin A': 5000,
            'Vitamin B1': 1.8,
            'Vitamin B2': 2.7,
            'Niacin': 18,
            'Vitamin C': 75
}

# Define the fitness function
def evaluate_fitness_base(scaling_factors):
    diet_plan = []
    for i, food in enumerate(foods):
        factor = scaling_factors[i]
        serving_size = factor * foods[food]["serving_size"]
        nutrients = {
            "carbohydrates": factor * foods[food]["carbohydrates"],
            "protein": factor * foods[food]["protein"],
            "fat": factor * foods[food]["fat"]
        }
        diet_plan.append({"food": food, "serving_size": serving_size, "nutrients": nutrients})
    # Calculate the macronutrient ratio of the diet plan
    total_carbs = sum(item["nutrients"]["carbohydrates"] for item in diet_plan)
    total_protein = sum(item["nutrients"]["protein"] for item in diet_plan)
    total_fat = sum(item["nutrients"]["fat"] for item in diet_plan)
    total_calories = (total_carbs + total_protein) * 4 + total_fat * 9
    ratio = {
        "carbohydrates": total_carbs / total_calories,
        "protein": total_protein / total_calories,
        "fat": total_fat / total_calories
    }
    # Calculate the fitness based on the proximity of the ratio to the target ratio
    diff = np.array([ratio[key] - target_ratio[key] for key in ratio])
    return -np.dot(diff, diff)  # Negative squared difference as fitness (maximization)


# Define the genetic algorithm
def genetic_algorithm(num_generations, population_size, mutation_rate):
    # Initialize the population
    population = []
    for i in range(population_size):
        scaling_factors = [random.uniform(*gene_range) for _ in range(num_genes)]
        fitness = evaluate_fitness(scaling_factors)
        individual = {"scaling_factors": scaling_factors, "fitness": fitness}
        population.append(individual)
    # Evolve the population
    for generation in range(num_generations):
        # Select parents using tournament selection
        parents = []
        for i in range(population_size):
            tournament = random.sample(population, 2)
            parents.append(max(tournament, key=lambda x: x["fitness"]))
        # Generate offspring using uniform crossover and mutation
        offspring = []
        for i in range(population_size):
            parent1 = parents[i]
            parent2 = random.choice(parents)
            scaling_factors = []
            for j in range(num_genes):
                if random.random() < 0.5:
                    scaling_factors.append(parent1["scaling_factors"][j])
                else:
                    scaling_factors.append(parent2["scaling_factors"][j])
                if random.random() < mutation_rate:
                    scaling_factors[j] += random.uniform(-0.1, 0.1)
                    scaling_factors[j] = max(min(scaling_factors[j], gene_range[1]), gene_range[0])
            fitness = evaluate_fitness(scaling_factors)
            offspring.append({"scaling_factors": scaling_factors, "fitness": fitness})
        # Replace the old population with the new offspring
        population = offspring
    # Return the best individual
    return max(population, key=lambda x: x["fitness"])



