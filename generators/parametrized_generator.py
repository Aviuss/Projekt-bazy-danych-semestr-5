import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.input_output import InputOutput
from typing import List, Dict
import math
import random
import numpy as np
import pandas as pd


class ParametrizedGenerator(InputOutput):
    def __init__(self, S, N, R, KO, CN, K=2, KI = 1, dimensions = 24, D=0):
        self.list_of_load_vectors: List[List[None | int]] = [None] * S
        self.S: int = S
        self.N: int = N
        self.K: int = K
        self.D: float = D
        self.R: float = R
        self.KO: float = KO
        self.KI: float = KI
        self.CN: int = CN
        self.dimensions: int = dimensions
        
    
    def generate(self) -> pd.DataFrame:

        shards_groups: List[Dict[str,int | float]] = [{"shard_index": [], "amplitude": 0.0, "offset_x": 0.0} for _ in range(self.K)]
        vectors_amplitude = [0.0] * self.S

        def assign_to_groups() -> list[int]:
            base_size = self.S // self.K
            sizes = [base_size] * self.K

            rest = self.S % self.K
            for i in range(rest):
                sizes[i] += 1

            current_sd = np.std(sizes)
            iteration = 0
            max_iterations = 1000

            while abs(current_sd - self.D) > 0.1 and iteration < max_iterations and self.D != 0:
                iteration += 1

                if current_sd < self.D:
                    sizes = sorted(sizes)
                    for i in range(self.K):
                        if sizes[i] > 0:
                            sizes[i] -= 1
                            break
                    sizes[-1] += 1

                elif current_sd > self.D:
                    sizes = sorted(sizes, reverse=True)
                    for i in range(self.K):
                        if sizes[i] > 0:
                            sizes[i] -= 1
                            break
                    sizes[-1] += 1

                current_sd = np.std(sizes)

            current_group = 0
            result = []
            for size in sizes:
                result.extend([current_group] * size)
                current_group += 1

            print("Final standard deviation:", current_sd)
            return result

        groups_assignment = assign_to_groups()
        print("Group assignment:", groups_assignment)
        for i in range(self.S):
            group_index = groups_assignment[i]
            shards_groups[group_index]["shard_index"].append(i)

        def calculate_KO(offset1, offset2, a1, a2, n_points=1000) -> float:
            t = np.linspace(0, 2*np.pi * self.CN, n_points)

            sinusoid1 = a1 * np.sin(t + offset1)
            sinusoid2 = a2 * np.sin(t + offset2)
            
            corr_matrix = np.corrcoef(sinusoid1, sinusoid2)
            
            correlation_value = corr_matrix[0, 1]
            return correlation_value
        
        for i in range(self.K):
            amplitude = random.uniform(0, 1)
            offset_x = random.uniform(0, 2*math.pi)
            shards_groups[i]["amplitude"] = amplitude
            shards_groups[i]["offset_x"] = offset_x
            var = (amplitude * self.R)**2 

            for shard_index in shards_groups[i]["shard_index"]:
                vectors_amplitude[shard_index] = np.random.lognormal(mean=amplitude, sigma=math.sqrt(var))
        
        curr_KO = 0.0
        offset1 = shards_groups[0]["offset_x"]
        amplitude1 = shards_groups[0]["amplitude"]
        offset2 = shards_groups[1]["offset_x"]
        amplitude2 = shards_groups[1]["amplitude"]
        while (abs(self.KO - curr_KO)>0.001):
            offset1 += 0.01
            offset1 = offset1 % (2*math.pi) 
            curr_KO = calculate_KO(offset1, offset2, amplitude1, amplitude2)
            shards_groups[0]["offset_x"] = offset1
        
        for i in range(self.K):
            for shard_index in shards_groups[i]["shard_index"]:
                load_vector:List[float] = [None] * self.dimensions
                amplitude = vectors_amplitude[shard_index]
                offset_x = shards_groups[i]["offset_x"]
                for d in range(self.dimensions):
                    x = (2 * math.pi * self.CN * d) / self.dimensions
                    load_vector[d] = amplitude * math.sin(x + offset_x)+ amplitude
                self.list_of_load_vectors[shard_index] = load_vector
        return pd.DataFrame(self.list_of_load_vectors)
    
    def print_results(self):
        print("Generated Load Vectors:")
        for i, vector in enumerate(self.list_of_load_vectors):
            print(f"Shard {i}: {vector}")
    

