import math
import random
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.input_output import InputOutput
from typing import List, Dict


class ExpRandomGenerator(InputOutput):
    def __init__(self, shard_count, dimensions=24, lambda_value=1):
        self.list_of_load_vectors: List[List[None | int]] = [None] * shard_count
        self.shard_count: int = shard_count
        self.lambda_value: int | float = lambda_value
        self.dimensions: int = dimensions

    def generate(self) -> pd.DataFrame:
        for i in range(self.shard_count):
            self.list_of_load_vectors[i]: List[List[None | int]] = [None] * self.dimensions
            for j in range(self.dimensions):
                self.list_of_load_vectors[i][j]: List[List[None | int]] = random.expovariate(self.lambda_value)
        return pd.DataFrame(self.list_of_load_vectors)

    def print_results(self):
        for vector, load_vector in enumerate(self.list_of_load_vectors):
            print(f'vector {vector}:', [value for value in load_vector])
