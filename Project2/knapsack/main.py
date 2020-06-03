from knapsack.generation import GenerationManager, GenerationStrategy
from knapsack.genetic_algorithm import GeneticAlgorithmFacade
from knapsack.mutation import Mutation, MutationStrategy
from knapsack.problem import KnapsackProblem, ProblemType
from knapsack.reproduction import Reproduction, ReproductionStrategy
from knapsack.selection import Selection, SelectionStrategy

class Config:
    def __init__(self):
        pass


if __name__ == "__main__":
    # GA variables
    generations = 100
    population_size = 100
    crossover_probability = 0.8
    mutation_probability = 0.2

    config=Config
    config.problem=KnapsackProblem(type=ProblemType.MAXIMIZATION,
                    values=[0, 1],
                    costs=[100, 350, 200, 90, 500, 250, 220, 360, 150, 700, 400, 230, 550],
                    weights=[50, 90, 30, 40, 100, 70, 20, 80, 80, 90, 50, 30, 70],
                    cargo=600)
    selection=Selection(config.problem, SelectionStrategy.TOURNAMENT_BATTLE_ROYALE)
    reproduction=Reproduction(ReproductionStrategy.SEXUAL_SINGLE_POINT, crossover_probability)
    mutation=Mutation(MutationStrategy.GENERATIVE, mutation_probability)

    config.generation=GenerationManager(config.problem, GenerationStrategy.EXCHANGE, selection, reproduction, mutation)
    config.population_size=100
    config.generations=100

    GeneticAlgorithmFacade(config).execute()