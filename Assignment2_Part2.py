import random
import time


def populate(size, N):
    population = []
    for i in range(size):
        population.append(new_individual(N))

    return population


def calc_fitness(individual):
    N = len(individual)
    queen_pairs = (N * (N - 1)) // 2

    attack_queens = 0
    for i in range(N):
        for j in range(i + 1, N):
            row1 = individual[i]
            row2 = individual[j]

            if row1 == row2:
                attack_queens += 1
            elif abs(row1 - row2) == abs(i - j):
                attack_queens += 1

    return queen_pairs - attack_queens


def get_fitness(population):
    fitness = []
    for i in population:
        fitness.append(calc_fitness(i))

    return fitness


def best_sol_fit(population, fitness):
    max_fit = max(fitness)
    index = fitness.index(max_fit)

    return population[index], max_fit


def maximum_fitness(N):
    return (N * (N - 1)) // 2


def sel_individual(population, fitness):
    total_fit = sum(fitness)

    if total_fit == 0:
        return random.choice(population)

    rand = random.uniform(0, total_fit)
    cur_sum = 0.0

    for i, j in zip(population, fitness):
        cur_sum += j
        if cur_sum >= rand:
            return i

    return population[-1]


def reproduce(first_parent, second_parent):
    N = len(first_parent)
    point = random.randint(1, N - 1)
    first_child = first_parent[:point] + second_parent[point:]
    second_child = second_parent[:point] + first_parent[point:]

    return first_child, second_child


def new_individual(N):
    individual = list(range(N))
    random.shuffle(individual)
    return individual


def mutate(child, mut_rate):
    N = len(child)
    for i in range(N):
        if random.random() < mut_rate:
            child[i] = random.randint(0, N - 1)

    return child


def n_queens_ga(N):
    size = 100
    max_generation = 2000
    mut_rate = 0.05

    starting_time = time.time()
    population = populate(size, N)
    fitness = get_fitness(population)

    solution, best_fitness = best_sol_fit(population, fitness)
    total_gen = 0
    best_sol = [(0, best_fitness, solution[:])]

    no_change_max = 100
    no_change_gen = 0

    max_fit = maximum_fitness(N)
    num_gen = 0
    while num_gen < max_generation and best_fitness < max_fit and no_change_gen < no_change_max:
        num_gen += 1
        new_pop = []

        for i in range(size // 2):
            first_parent = sel_individual(population, fitness)
            second_parent = sel_individual(population, fitness)
            first_child, second_child = reproduce(first_parent, second_parent)
            first_child = mutate(first_child, mut_rate)
            second_child = mutate(second_child, mut_rate)

            new_pop.append(first_child)
            new_pop.append(second_child)

        if len(new_pop) < size:
            new_pop.append(new_individual(N))

        population = new_pop
        fitness = get_fitness(population)
        current_sol, current_fit = best_sol_fit(population, fitness)

        if current_fit > best_fitness:
            best_fitness = current_fit
            solution = current_sol[:]
            total_gen = num_gen

        best_sol.append((num_gen, current_fit, current_sol[:]))
        if best_fitness == max_fit:
            break

    time_elapsed = time.time() - starting_time
    return solution, total_gen, best_sol, time_elapsed


def display(solution):
    N = len(solution)

    for i in range(N):
        row = ""

        for j in range(N):
            if solution[j] == i:
                row += "Q "
            else:
                row += "_ "

        print(row)


while True:
    N = int(input("Enter a value for N (4 <= N <= 20). Enter 0 to stop: "))

    if N == 0:
        break
    if N < 4 or N > 20:
        print("Invalid Value - N needs to be >= 4 and <= 20. Enter 0 to stop: ")
        continue

    solution, generation, sol_max_fit, run_time = n_queens_ga(N)

    print()
    print(f"For N = {N}. Found at Generation = {generation}")
    display(solution)
    print()
    print(f"The Run Time to find the solution: {run_time} seconds")
    print()
    print("Maximum Fitness in all past generation and solutions with highest fitness values: ")

    for generation, fitness, best_solution in sol_max_fit:
        print(f"Maximum Fitness: {fitness}")
        print(f"Best Solution: {best_solution}")
        print(f"Generation: {generation}")
