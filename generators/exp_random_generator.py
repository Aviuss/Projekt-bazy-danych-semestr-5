import math
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.input_output import InputOutput

class ExpRandomGenerator:
    def __init__(self, shard_count, dimensions = 24, lambda_value = 1):
        self.list_of_load_vectors = [None] * shard_count
        self.shard_count = shard_count
        self.lambda_value = lambda_value
        self.dimensions = dimensions

    def generate(self):
        for i in range(self.shard_count):
            self.list_of_load_vectors[i] = [None] * self.dimensions
            for j in range(self.dimensions):
                self.list_of_load_vectors[i][j] = random.expovariate(self.lambda_value)
        return self.list_of_load_vectors

    def print_results(self):
        for vector, load_vector in enumerate(self.list_of_load_vectors):
            print(f'vector {vector}:',[round(value, 4) for value in load_vector])
    
    def save_results(self, filename):
        InputOutput().save_to_csv_file(self.list_of_load_vectors, filename)
