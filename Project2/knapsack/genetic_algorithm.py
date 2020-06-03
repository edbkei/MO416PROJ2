class GeneticAlgorithmFacade:
    def __init__(self, config):
        self.config = config

    def execute(self):
        population = self.config.generation.generate_population(self.config.population_size,
                                                                self.config.problem.values,
                                                                self.config.problem.population_length)

        i = 1
        while True:
            print(f"Generation {i}")

            for individual in population:
                print(individual, "Fitness:", self.config.problem.getFitness(individual),
                      "Cost:", self.config.problem.apply_costs(individual),
                      "Cargo:", self.config.problem.apply_weights(individual))

            best_fitness = self.config.problem.getFitness(self.config.generation.sort_population_by_fitness(population)[-1])
            worst_fitness = self.config.problem.getFitness(self.config.generation.sort_population_by_fitness(population)[0])
            mean_fitness = self.config.problem.meanFitness(population)

            print()
            print("Best:", best_fitness,
                  "Mean:", mean_fitness,
                  "Worst:", worst_fitness)
            print()

            if i == self.config.generations:
                break

            i += 1

            population = self.config.generation.next_generation(population)

        best_individual = self.config.generation.sort_population_by_fitness(population)[-1]
        print("\nBest choice: ")
        print(best_individual, "Fitness:", self.config.problem.getFitness(best_individual),
                      "Cost:", self.config.problem.apply_costs(best_individual),
                      "Cargo:", self.config.problem.apply_weights(best_individual))