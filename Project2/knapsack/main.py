from generation import GenerationStrategy
from genetic_algorithm import GeneticAlgorithmFacade
from mutation import MutationStrategy
from problem import ProblemType
from reproduction import ReproductionStrategy
from selection import SelectionStrategy

import matplotlib.pyplot as plt

from knapsack.genetic_algorithm import StopCriteriaType

def plot_fitness(generationsResult):
    best = list(map(lambda result: result["best"], generationsResult))
    mean = list(map(lambda result: result["mean"], generationsResult))
    worst = list(map(lambda result: result["worst"], generationsResult))
    plt.plot(best, label="best")
    plt.plot(mean, label="mean")
    plt.plot(worst, label="worst")

    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Knapsack Problem")
    plt.legend(loc='lower left', frameon=True)

    plt.show()

if __name__ == "__main__":
    config = {
        'problem': {
            'type': ProblemType.MAXIMIZATION,
            'values': [0, 1],
            'costs': [100, 350, 200, 90, 500, 250, 220, 360, 150, 700, 400, 230, 550],
            'weights': [50, 90, 30, 40, 100, 70, 20, 80, 80, 90, 50, 30, 70],
            'cargo': 600
        },
        'selection': {
            'strategy': SelectionStrategy.ROULETTE
        },
        'reproduction': {
            'strategy': ReproductionStrategy.SEXUAL_SINGLE_POINT,
            'rate': 0.8
        },
        'mutation': {
            'strategy': MutationStrategy.SEQUENCE_SWAP,
            'rate': 0.2
        },
        'generation': {
            'strategy': GenerationStrategy.ELITISM,
            #'substituted_population_size': 10, #Used only on STEADY_STATE
            'population_size': 25,
        },
        'stop_criteria': {
            #'fitness': 0, #Used only on MAX_FITNESS
            'num_generations': 100,
            'type': StopCriteriaType.MAX_GENERATIONS
        }
    }

    generationsResult = GeneticAlgorithmFacade(config).execute()

    plot_fitness(generationsResult)