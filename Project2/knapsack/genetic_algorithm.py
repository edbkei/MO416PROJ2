from knapsack. stop_criteria import StopCriteriaType

class GeneticAlgorithmFacade:
    def __init__(self, config):
        self.config = config

    def execute(self):
        fo1=open("file1.txt","w")
        fo2=open("file2.txt","w")

        population = self.config.generation.generate_population(self.config.population_size,
                                                                self.config.problem.values,
                                                                self.config.problem.population_length)
        results = []
        best_individual = None
        i = 1
        countBreak=1
        countPeriod = 1
        print("Processing ...generating file1.txt for graphics and file2.txt for detailed population generations")
        while True:
            arg="Generation {"+str(i)+"}"+"\n"
            fo2.write(arg)

            for individual in population:
                arg=str(individual)+" Fitness: "+str(self.config.problem.getFitness(individual))+ \
                      " Cost: "+str(self.config.problem.apply_costs(individual))+ \
                      " Cargo: "+str(self.config.problem.apply_weights(individual))+"\n"
                fo2.write(arg)

            sorted_population = self.config.generation.sort_population_by_fitness(population)

            best_fitness, _, _ = self.add_stats(fo1, fo2, i, sorted_population, results)

            population = self.config.generation.next_generation(population, num_new_individuals=self.config.substituted_population_size)

            best_gen_ind = sorted_population[-1]
            print(best_gen_ind, self.config.problem.getFitness(best_gen_ind))
            if best_individual != None: print(best_individual, self.config.problem.getFitness(best_individual))
            if best_individual == None or self.config.generation.selection.compareFitness(best_gen_ind, best_individual):
                best_individual = best_gen_ind[:]
                countPeriod = 1
            else:
                countPeriod += 1

            if self.stop_criteria(generation=i, period=countPeriod, fitness=best_fitness, population=sorted_population):
                countBreak=i
                break

            i += 1

        print("\nBest choice: ")
        print(best_individual, "- Fitness:", self.config.problem.getFitness(best_individual),
                      "- Cost:", self.config.problem.apply_costs(best_individual),
                      "- Cargo:", self.config.problem.apply_weights(best_individual),
                      "- Generations at stop criteria:", countBreak)

        fo1.close()
        fo2.close()

        return results

    def stop_criteria(self, generation=None, period=None, fitness=None, population=None):
        if self.config.stop_criteria.type == StopCriteriaType.MAX_GENERATIONS:
            return generation == self.config.stop_criteria.num_generations
        elif self.config.stop_criteria.type == StopCriteriaType.MAX_FITNESS:
            return fitness == self.config.stop_criteria.fitness
        elif self.config.stop_criteria.type == StopCriteriaType.CONVERGENCE:
            num_best = round(self.config.stop_criteria.quorum * len(population))
            count = sum(self.config.problem.getFitness(pop) == fitness for pop in population)

            return count >= num_best
        elif self.config.stop_criteria.type == StopCriteriaType.STEADY_PERIOD:
            return period == self.config.stop_criteria.num_generations
        else:
            self.invalid()

    def invalid(self):
        raise Exception("Invalid criteria")

    def add_stats(self, fo1, fo2, i, sorted_population, results):
        best_fitness = self.config.problem.getFitness(sorted_population[-1])
        j = 0
        worst_fitness = -1
        while(worst_fitness < 0):
            worst_fitness = self.config.problem.getFitness(sorted_population[j])
            j += 1
        mean_fitness = self.config.problem.meanFitness(sorted_population)

        fo2.write("\n")
        arg = "Best: " + str(best_fitness) + \
              " Mean: " + str(mean_fitness) + \
              " Worst: " + str(worst_fitness) + "\n"
        fo2.write(arg)
        fo2.write("\n")
        arg = str(i) + "," + str(best_fitness) + "," + str(mean_fitness) + "," + str(worst_fitness) + "\n"
        fo1.write(arg)

        results.append({
            'best': best_fitness,
            'mean': mean_fitness,
            'worst': worst_fitness
        })

        return best_fitness, mean_fitness, worst_fitness