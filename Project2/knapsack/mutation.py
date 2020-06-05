import random
from enum import IntEnum

class MutationStrategy(IntEnum):
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
        while True:
            sequence_swap_init = random.randint(0, n - 2)
            sequence_swap_final = random.randint(sequence_swap_init, n - 1)
            if sequence_swap_init != 0 and sequence_swap_final != n - 1:
                break

        remaining = list(range(0, sequence_swap_init)) + list(range(sequence_swap_final+1, n))
        swapWith = random.choice(remaining)

        if swapWith < sequence_swap_init:
            print(sequence_swap_final)
            individual = [] + individual[0:swapWith]\
                + individual[sequence_swap_init:sequence_swap_final + 1]\
                + individual[swapWith:sequence_swap_init]\
                + individual[(sequence_swap_final + 1):len(individual)]
        else:
            print(swapWith)
            individual = [] + individual[0:sequence_swap_init]\
                + individual[(sequence_swap_final + 1):swapWith + 1]\
                + individual[sequence_swap_init:sequence_swap_final + 1]\
                + individual[(swapWith + 1):len(individual)]

        return individual
