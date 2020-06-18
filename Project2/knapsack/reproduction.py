import random
from enum import IntEnum


class ReproductionStrategy(IntEnum):
    ASEXUAL = 1,
    SEXUAL_SINGLE_POINT = 2,
    SEXUAL_DOUBLE_POINTS = 3

class Reproduction:
    def __init__(self, strategy, rate):
        self.strategy = strategy
        self.rate = rate

    def execute(self, individual_a, individual_b=None):
        if self.strategy == ReproductionStrategy.ASEXUAL:
            return self.duplication(individual_a)
        elif self.strategy == ReproductionStrategy.SEXUAL_SINGLE_POINT:
            return self.crossover_single_point(individual_a, individual_b)
        elif self.strategy == ReproductionStrategy.SEXUAL_DOUBLE_POINTS:
            return self.crossover_double_points(individual_a, individual_b)
        else:
            self.invalid()

    def invalid(self):
        raise Exception("Invalid reproduction")

    def duplication(self, individual):
        return individual[:]

    def crossover_single_point(self, individual_a, individual_b):
        n = len(individual_a)
        c = random.randint(0, n - 1)
        return individual_a[0:c] + individual_b[c:n]

    def crossover_double_points(self, individual_a, individual_b):
        n = len(individual_a)
        c1 = random.randint(0, n - 2)
        c2 = random.randint(c1, n - 1)
        return individual_a[0:c1] + individual_b[c1:c2] + individual_a[c2:n]
