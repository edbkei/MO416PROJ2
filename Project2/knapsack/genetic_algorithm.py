from knapsack. stop_criteria import StopCriteriaType

class GeneticAlgorithmFacade:
    def __init__(self, config):
        self.config = config

    def execute(self):
        population = self.config.generation.generate_population(self.config.population_size,
                                                                self.config.problem.values,
                                                                self.config.problem.population_length)
        results = []
        best_individual = None

        i = 1
        while True:
            print(f"Generation {i}")

            for individual in population:
                print(individual, "Fitness:", self.config.problem.getFitness(individual),
                      "Cost:", self.config.problem.apply_costs(individual),
                      "Cargo:", self.config.problem.apply_weights(individual))

            sorted_population = self.config.generation.sort_population_by_fitness(population)

            best_fitness = self.config.problem.getFitness(sorted_population[-1])
            worst_fitness = self.config.problem.getFitness(sorted_population[0])
            mean_fitness = self.config.problem.meanFitness(population)

            print()
            print("Best:", best_fitness,
                  "Mean:", mean_fitness,
                  "Worst:", worst_fitness)
            print()

            results.append({
                'best': best_fitness,
                'mean': mean_fitness,
                'worst': worst_fitness
            })

            population = self.config.generation.next_generation(population, num_new_individuals=self.config.substituted_population_size)

            best_gen_ind = sorted_population[-1]
            if best_individual == None or self.config.generation.selection.compareFitness(best_gen_ind, best_individual):
                best_individual = best_gen_ind

            if self.stop_criteria(generation=i, fitness=best_fitness, population=sorted_population):
                break

            i += 1

        print("\nBest choice: ")
        print(best_individual, "Fitness:", self.config.problem.getFitness(best_individual),
                      "Cost:", self.config.problem.apply_costs(best_individual),
                      "Cargo:", self.config.problem.apply_weights(best_individual))

        return results

    def stop_criteria(self, generation=None, fitness=None, population=None):
        if self.config.stop_criteria.type == StopCriteriaType.MAX_GENERATIONS:
            return generation == self.config.stop_criteria.num_generations
        elif self.config.stop_criteria.type == StopCriteriaType.MAX_FITNESS:
            return fitness == self.config.stop_criteria.fitness
        elif self.config.stop_criteria.type == StopCriteriaType.CONVERGENCE:
            num_best = round(self.config.stop_criteria.quorum * len(population))
            count = sum(self.config.problem.getFitness(pop) == fitness for pop in population)

            return count >= num_best
        else:
            self.invalid()

    def invalid(self):
        raise Exception("Invalid criteria")