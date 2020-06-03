import random
from enum import Enum

class GenerationStrategy(Enum):
    EXCHANGE = 1,
    ELITISM = 2,
    STEADY_STATE = 3

class GenerationManager:
    def __init__(self, problem, strategy, selection, reproduction, mutation):
        self.problem = problem
        self.strategy = strategy
        self.selection = selection
        self.reproduction = reproduction
        self.mutation = mutation

    def next_generation(self, previous_population, num_new_individuals=None, values=None):
        if self.strategy == GenerationStrategy.EXCHANGE:
            return self.by_entire_exchange(previous_population)
        elif self.strategy == GenerationStrategy.ELITISM:
            return self.by_elitism(previous_population)
        elif self.strategy == GenerationStrategy.STEADY_STATE:
            return self.by_steady_state(previous_population, num_new_individuals, values)
        else:
            self.invalid()

    def invalid(self):
        raise Exception("Invalid generation")

    def sort_population_by_fitness(self, population):
        return sorted(population, key=self.problem.getFitness)

    def generate_population(self, size, values, length):
        population = []

        for i in range(0, size):
            pop = random.choices(values, k=length)

            population.append(pop)
        return population

    def make_next_generation(self, previous_population):
        next_generation = []
        sorted_by_fitness_population = self.sort_population_by_fitness(previous_population)
        population_size = len(previous_population)

        while (len(next_generation) < population_size):
            cross_prob = random.random()
            mut_prob = random.random()
            if cross_prob < self.reproduction.rate:
                first_choice, second_choice = self.selection.execute(sorted_by_fitness_population, single=False)

                individual = self.reproduction.execute(first_choice, second_choice)
            else:
                individual = self.selection.execute(sorted_by_fitness_population)

            if mut_prob < self.mutation.rate:
                individual = self.mutation.execute(individual)

            next_generation.append(individual)

        return next_generation

    def by_entire_exchange(self, previous_population):
        return self.make_next_generation(previous_population)

    def by_elitism(self, previous_population):
        next_generation = self.make_next_generation(previous_population)

        individual_to_swap = self.sort_population_by_fitness(next_generation)[0]
        best_previous_individual = self.sort_population_by_fitness(previous_population)[-1]

        next_generation[next_generation.index(individual_to_swap)] = best_previous_individual

        return next_generation

    def by_steady_state(self, previous_population, num_new_individuals, values):
        next_generation = self.make_next_generation(previous_population)

        example_individual = next_generation[0]
        new_individuals = self.generate_population(num_new_individuals, values, len(example_individual))

        for i in range(len(next_generation) - len(new_individuals) - 1, len(next_generation)):
            next_generation[i] = new_individuals[i - len(next_generation) - len(new_individuals) - 1]

        return next_generation