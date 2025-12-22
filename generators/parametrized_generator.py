import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.input_output import InputOutput
from typing import List, Dict
import math
import random
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution


class ParametrizedGenerator(InputOutput):
    def __init__(self, S, N, R, KO, CN, K=2, KI=1, dimensions=24, D=0):
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
        vectors_offset_x = [0.0] * self.S

        groups_assignment = self.assign_to_groups()
        print("Group assignment:", groups_assignment)

        for i in range(self.S):
            group_index = groups_assignment[i]
            shards_groups[group_index]["shard_index"].append(i)


        for i in range(self.K):
            amplitude = random.uniform(0, 1)
            offset_x = random.uniform(0, 2*math.pi)
            shards_groups[i]["amplitude"] = amplitude
            shards_groups[i]["offset_x"] = offset_x
            var = (amplitude * self.R)**2 

            for shard_index in shards_groups[i]["shard_index"]:
                vectors_amplitude[shard_index] = np.random.lognormal(mean=amplitude, sigma=math.sqrt(var))
        
            amplitude_group = [vectors_amplitude[shard_index] for shard_index in shards_groups[i]["shard_index"]]
            if (len(amplitude_group) == 0):
                print("Uwaga! Pewna grupa jest pusta. Najlepiej jakbyś dostosował parametry")
                continue
            inside_group_offsets = self.calculate_KX(self.KI, amplitude_group)
            
            for iiii in range(len(shards_groups[i]["shard_index"])):
                shard_index = shards_groups[i]["shard_index"][iiii]
                vectors_offset_x[shard_index] = inside_group_offsets[iiii]
                

        amplitudes = [shards_groups[i]["amplitude"] for i in range(self.K)]
        offsets_between_groups = self.calculate_KX(self.KO, amplitudes)
        for i in range(self.K):
            group_offset = offsets_between_groups[i]
            for iiii in range(len(shards_groups[i]["shard_index"])):
                shard_index = shards_groups[i]["shard_index"][iiii]
                vectors_offset_x[shard_index] += group_offset


        for i in range(self.K):
            for shard_index in shards_groups[i]["shard_index"]:
                load_vector:List[float] = [None] * self.dimensions
                amplitude = vectors_amplitude[shard_index]
                offset_x = vectors_offset_x[shard_index]

                for d in range(self.dimensions):
                    x = (2 * math.pi * self.CN * d) / self.dimensions
                    load_vector[d] = amplitude * math.sin(x + offset_x)
                self.list_of_load_vectors[shard_index] = load_vector
        return pd.DataFrame(self.list_of_load_vectors)
    

    def calculate_KX(self, kx, amplitude_list: List[float], n_points=500) -> List[float]:
        n = len(amplitude_list)

        target_KO_Matrix = np.full((n, n), kx)
        np.fill_diagonal(target_KO_Matrix, 1)
        
        def calculate_load_base_group(offset, amplitude):
            t = np.linspace(0, 2*np.pi * self.CN, n_points)
            sinusoid = amplitude * np.sin(t + offset)
            return sinusoid

        def cost(offsets: List[float]) -> int:
            vectors = []
            for i in range(len(amplitude_list)):
                vectors.append(calculate_load_base_group(offsets[i], amplitude_list[i]))
            vectors = np.array(vectors)
            corr_matrix = np.corrcoef(vectors)
            c = np.sum(np.abs(target_KO_Matrix - corr_matrix)**10)
                
            return c
    
        bounds = [(0, 2*np.pi)] * n

        result = differential_evolution(cost, bounds, strategy='currenttobest1bin', maxiter=200, popsize=16, recombination=0.3, tol=1e-6, mutation=0.3)   

        best_offsets = result.x
        vectors_opt = np.array([calculate_load_base_group(o, a) for o, a in zip(best_offsets, amplitude_list)])
        corr_matrix_opt = np.corrcoef(vectors_opt)

        print("KO DEBUG == START == ")
        print("Best offsets:", best_offsets)
        print("Target Kx:", kx)
        print("Optimized correlation matrix:\n", np.round(corr_matrix_opt, 2))
        print("Average correlation", (np.sum(corr_matrix_opt) - n)/(n*n - n))
        print("KO DEBUG ==  END  == ")

        return best_offsets

    def assign_to_groups(self) -> list[int]:
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

    def print_results(self):
        print("Generated Load Vectors:")
        for i, vector in enumerate(self.list_of_load_vectors):
            print(f"Shard {i}: {vector}")
    

if __name__ == "__main__":
    generator = ParametrizedGenerator(S=10, N=5, R=0.5, KO=0.7, CN=3, K=2, KI=1, dimensions=24, D=1.0)
    df = generator.generate()
    generator.print_results()
    print(df)