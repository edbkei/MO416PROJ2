from generation import GenerationManager
from mutation import Mutation
from problem import KnapsackProblem
from reproduction import Reproduction
from selection import Selection
from stop_criteria import StopCriteriaType, StopCriteria


class Config:
    def __init__(self):
        pass

class GeneticAlgorithmFacade:
    def __init__(self, config):
        self.config = self.create_configuration(config)

    def create_configuration(self,configDict):
        config = Config
        config.problem = KnapsackProblem(type=configDict['problem']['type'],
                                         values=configDict['problem']['values'],
                                         costs=configDict['problem']['costs'],
                                         weights=configDict['problem']['weights'],
                                         cargo=configDict['problem']['cargo'])

        selection = Selection(config.problem, configDict['selection']['strategy'])
        reproduction = Reproduction(configDict['reproduction']['strategy'], configDict['reproduction']['rate'])
        mutation = Mutation(configDict['mutation']['strategy'], configDict['mutation']['rate'])
        config.generation = GenerationManager(config.problem, configDict['generation']['strategy'],
                                              selection, reproduction, mutation)

        config.population_size = configDict['generation']['population_size']
        config.substituted_population_size = self.checkKeyAndReturn(configDict['generation'],
                                                                    'substituted_population_size')

        config.stop_criteria = StopCriteria(configDict['stop_criteria']['type'],
                                            self.checkKeyAndReturn(configDict['stop_criteria'], 'num_generations'),
                                            self.checkKeyAndReturn(configDict['stop_criteria'], 'fitness'))

        return config

    def checkKeyAndReturn(self, dict, key):
        return dict[key] if key in dict.keys() else None

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

            if self.stop_criteria(generation=i, fitness=best_fitness):
                break

            i += 1

            population = self.config.generation.next_generation(population, num_new_individuals=self.config.substituted_population_size)

            best_gen_ind = sorted_population[-1]
            if best_individual == None or self.config.generation.selection.compareFitness(best_gen_ind, best_individual):
                best_individual = best_gen_ind

        print("\nBest choice: ")
        print(best_individual, "Fitness:", self.config.problem.getFitness(best_individual),
                      "Cost:", self.config.problem.apply_costs(best_individual),
                      "Cargo:", self.config.problem.apply_weights(best_individual))

        return results

    def stop_criteria(self, generation=None, fitness=None):
        if self.config.stop_criteria.type == StopCriteriaType.MAX_GENERATIONS:
            return generation == self.config.stop_criteria.num_generations
        elif self.config.stop_criteria.type == StopCriteriaType.MAX_FITNESS:
            return fitness == self.config.stop_criteria.fitness
        else:
            self.invalid()

    def invalid(self):
        raise Exception("Invalid criteria")