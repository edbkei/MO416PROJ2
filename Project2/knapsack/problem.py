from enum import Enum

class ProblemType(Enum):
    MAXIMIZATION = 1,
    MINIMIZATION = 2,
    SOLVING = 3

class Problem:
    def __init__(self, type, values, length, maxFitness, steadyPeriod):
        self.type = type
        self.values = values
        self.population_length = length
        self.maxFitness = maxFitness
        self.steadyPeriod = steadyPeriod

    def getFitness(self, population):
        pass

class KnapsackProblem(Problem):
    def __init__(self, type, values, costs, weights, cargo, maxFitness, steadyPeriod):
        self.costs = costs
        self.weights = weights
        self.cargo = cargo
        super(KnapsackProblem, self).__init__(type, values, len(self.costs), maxFitness, steadyPeriod)
        self.validate()

    def validate(self):
        if (self.cargo < 0):
            raise Exception("Cargo should be positive")
        if (len(self.costs) <= 0 or len(self.weights) <= 0):
            raise Exception("Costs and Weights should have an item")
        if (len(self.costs) != len(self.weights)):
            raise Exception("Costs and Weights should have the same length")

    def validateIndividual(self, individual):
        return len(self.costs) == len(individual) \
               and len(self.weights) == len(individual) \
               and self.apply_weights(individual) <= self.cargo

    def getFitness(self, individual):
        if (self.validateIndividual(individual)):
            return self.apply_costs(individual)
        return -1

    def apply_costs(self, individual):
        cost = 0

        for i in range(0, len(individual)):
            cost += individual[i] * self.costs[i]

        return cost

    def apply_weights(self, individual):
        weight = 0

        for i in range(0, len(individual)):
            weight += individual[i] * self.weights[i]

        return weight

    def meanFitness(self, population):
        total = 0

        for i in range(0, len(population)):
            total += self.getFitness(population[i])

        return total / len(population)