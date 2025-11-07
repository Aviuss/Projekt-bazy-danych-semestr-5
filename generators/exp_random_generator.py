import math
import random

class Exp_random_generator:
    def __init__(self, shard_count):
        self.result_load_vectors = [None] * shard_count
        self.shard_count = shard_count
        self.lambda_value = 1
        self.dimensions = 24

    def generate(self):
        for i in range(self.shard_count):
            self.result_load_vectors[i] = [None] * self.dimensions
            for j in range(self.dimensions):
                self.result_load_vectors[i][j] = random.expovariate(self.lambda_value)
        return self.result_load_vectors