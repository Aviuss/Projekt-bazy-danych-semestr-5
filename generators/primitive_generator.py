import math

class Primitive_generator:
    def __init__(self, shard_count):
        self.result_load_vectors = [None] * shard_count
        self.shard_count = shard_count

    def generate(self):
        for i in range(self.shard_count):
            self.result_load_vectors[i] = [None] * 24
            for j in range(24):
                self.result_load_vectors[i][j] = self.rozklad_wykladniczy(j, 1)
        return self.result_load_vectors

    def rozklad_wykladniczy(self, x, lambda_value):
        if x < 0:
            return 0
        return lambda_value * (math.e ** (- lambda_value * x) )