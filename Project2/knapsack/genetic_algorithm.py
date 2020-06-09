class GeneticAlgorithmFacade:
    def __init__(self, config):
        self.config = config

    def execute(self):
        fo1=open("file1.txt","w")
        fo2=open("file2.txt","w")

        population = self.config.generation.generate_population(self.config.population_size,
                                                                self.config.problem.values,
                                                                self.config.problem.population_length)
        print("Processing ...")
        i = 1
        while True:
            arg="Generation {"+str(i)+"}"+"\n"
            fo2.write(arg)

            for individual in population:
                arg=str(individual)+" Fitness: "+str(self.config.problem.getFitness(individual))+ \
                      " Cost: "+str(self.config.problem.apply_costs(individual))+ \
                      " Cargo: "+str(self.config.problem.apply_weights(individual))+"\n"
                fo2.write(arg)

            best_fitness = self.config.problem.getFitness(self.config.generation.sort_population_by_fitness(population)[-1])
            worst_fitness = self.config.problem.getFitness(self.config.generation.sort_population_by_fitness(population)[0])
            mean_fitness = self.config.problem.meanFitness(population)

            fo2.write("\n")
            arg="Best: "+str(best_fitness)+ \
                  " Mean: "+ str(mean_fitness)+ \
                  " Worst: "+ str(worst_fitness)+"\n"
            fo2.write(arg)
            fo2.write("\n")
            arg=str(i)+","+str(best_fitness)+","+str(mean_fitness)+","+str(worst_fitness)+"\n"
            fo1.write(arg)

            if i == self.config.generations:
                break

            i += 1

            population = self.config.generation.next_generation(population)

        best_individual = self.config.generation.sort_population_by_fitness(population)[-1]
        print("\nBest choice: ")
        print(best_individual, "Fitness:", self.config.problem.getFitness(best_individual),
                      "Cost:", self.config.problem.apply_costs(best_individual),
                      "Cargo:", self.config.problem.apply_weights(best_individual))
        fo1.close()
        fo2.close()