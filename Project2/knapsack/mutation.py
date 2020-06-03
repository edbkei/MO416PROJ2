import random
from enum import Enum

class MutationStrategy(Enum):
    GENERATIVE = 1,
    SWAP = 2,
    SEQUENCE_SWAP = 3

class Mutation:
    def __init__(self, strategy, rate):
        self.strategy = strategy
        self.rate = rate

    def execute(self, individual):
        strategies = {
            MutationStrategy.GENERATIVE: self.generative(individual),
            MutationStrategy.SWAP: self.swap(individual),
            MutationStrategy.SEQUENCE_SWAP: self.sequence_swap(individual)
        }

        return strategies.get(self.strategy, self.invalid)

    def invalid(self):
        raise Exception("Invalid mutation")

    def generative(self, individual):
        n = len(individual)
        c = random.randint(0, n - 1)
        m = random.randint(0, 1)
        individual[c] = m
        return individual

    def swap(self, individual):
        n = len(individual)
        swapped = random.randint(0, n - 1)
        swapWith = random.randint(0, n - 1)

        aux = individual[swapped]
        individual[swapped] = individual[swapWith]
        individual[swapWith] = aux

        return individual

    # TODO verificar algoritmo
    def sequence_swap(self, individual):
        n = len(individual)
        swapped = random.randint(0, n - 1)
        swapWith = random.randint(0, n - 1)

        aux = individual[swapped]
        individual[swapped] = individual[swapWith]
        individual[swapWith] = aux

        return individual
