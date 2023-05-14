import random
import pandas as pd

foods = pd.read_excel("SDP_data.xlsx")
foods.set_index("Commodity", inplace = True)

# Define the number of genes (scaling factors)
num_genes = len(foods)

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



