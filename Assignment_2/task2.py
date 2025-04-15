import random

tasks = [1, 2, 3, 4, 5, 6, 7]
time = {1:5, 2:8, 3:4, 4:7, 5:6, 6:3, 7:9}
facilities = [1, 2, 3]
capacity = {1:24, 2:30, 3:28}
cost = {
    1: {1:10, 2:12, 3:9},
    2: {1:15, 2:14, 3:16},
    3: {1:8, 2:9, 3:7},
    4: {1:12, 2:10, 3:13},
    5: {1:14, 2:13, 3:12},
    6: {1:9, 2:8, 3:10},
    7: {1:11, 2:12, 3:13}
}

def generate_population(pop_size):
    return [[random.choice(facilities) for _ in range(7)] for _ in range(pop_size)]

def fitness(individual):
    total_cost = 0
    facility_time = {1: 0, 2: 0, 3: 0}
    
    for task, facility in zip(tasks, individual):
        task_time = time[task]
        total_cost += task_time * cost[task][facility]
        facility_time[facility] += task_time
    
    makespan = max(facility_time.values())
    
    penalty = 0
    for fac in facilities:
        if facility_time[fac] > capacity[fac]:
            penalty += 10000 * (facility_time[fac] - capacity[fac])
    
    # We want to minimize (total_cost + makespan + penalty), so return the negative
    return -(total_cost + makespan + penalty)

def roulette_wheel_selection(population, population_fitness):
    weights = [f + abs(min(population_fitness)) + 1 for f in population_fitness]
    p1 = random.choices(population, weights=weights, k=1)[0]
    p2 = random.choices(population, weights=weights, k=1)[0]
    while p1 == p2:  # Ensure distinct parents
        p2 = random.choices(population, weights=weights, k=1)[0]
    return p1, p2

def crossover(parent1, parent2, crossover_rate=0.8):
    if random.random() <= crossover_rate:
        crossover_point = random.randint(1, 6)  # Points between genes
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    return parent1.copy(), parent2.copy()

def mutate(individual, mutation_rate=0.2):
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

def genetic_algorithm(pop_size, generations):
    population = generate_population(pop_size)

    for _ in range(generations):
        population_fitness = [fitness(individual) for individual in population]
        new_population = []

        for _ in range(pop_size // 2): # To keep the population constant
            parent1, parent2 = roulette_wheel_selection(population, population_fitness)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1), mutate(child2)])
        population = new_population

    return max(population, key=fitness)

best_solution = genetic_algorithm(pop_size=6, generations=200)
print("Best solution:", best_solution)
print("Fitness:", fitness(best_solution))