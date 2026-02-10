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
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

class ParametrizedGenerator(InputOutput):
    def __init__(self, S, R, KO, CN, K=2, KI=1, dimensions=24, D=0, kx_error_threshold = 0.5):
        self.list_of_load_vectors: List[List[None | int]] = [None] * S
        self.S: int = S
        self.K: int = K
        self.D: float = D
        self.R: float = R
        self.KO: float = KO
        self.KI: float = KI
        self.CN: int = CN
        self.dimensions: int = dimensions
        self.shards_groups = []
        self.vectors_amplitude = []
        self.vectors_offset_x = []
        self.kx_error_threshold = kx_error_threshold

    def create_plots(self):
        RESOLUTION = 5
        N = self.dimensions * RESOLUTION
        d = np.linspace(0, self.dimensions - 1, N)
        highest_amplitude = 0
        for i in range(self.K):
            for shard_index in self.shards_groups[i]["shard_index"]:
                amplitude = self.vectors_amplitude[shard_index]
                highest_amplitude = max(highest_amplitude, amplitude)

        vectors_grouped = []
        for shards_in_group in self.shards_groups:
            vectors_grouped.append([])
            for shard_index in shards_in_group["shard_index"]:
                amplitude = self.vectors_amplitude[shard_index]
                offset_x = self.vectors_offset_x[shard_index]

                x = (2 * math.pi * self.CN * d) / self.dimensions

                load_vector = amplitude * np.sin(x + offset_x) + highest_amplitude
                vectors_grouped[len(vectors_grouped)-1].append(load_vector)


        colors = plt.cm.hsv(np.linspace(0, 1, len(vectors_grouped), endpoint=False))
        plt.figure(figsize=(10, 5))

        ox = np.linspace(1, self.dimensions, N)
        for group_idx, group in enumerate(vectors_grouped):
            for vec_idx, vec in enumerate(group):
                label = f"Grupa {group_idx+1}" if vec_idx == 0 else None
                plt.plot(ox, vec, color=colors[group_idx], alpha=0.33, label=label)

        plt.legend()
        plt.title(f"S={self.S}; K={self.K}; KO={self.KO}; KI={self.KI}; R={self.R}; D={self.D}; CN={self.CN}")
        plt.xticks(np.arange(1, self.dimensions+1, 1))
        plt.grid(True)
        plt.xlabel("wektor obciążeń")
        plt.ylabel("średnie obciążenie")
        plt.show()


    def generate(self) -> pd.DataFrame:
        self.shards_groups: List[Dict[str,int | float]] = [{"shard_index": [], "amplitude": 0.0, "offset_x": 0.0} for _ in range(self.K)]
        self.vectors_amplitude = [0.0] * self.S
        self.vectors_offset_x = [0.0] * self.S

        groups_assignment = self.assign_to_groups()
        print("Group assignment:", groups_assignment)

        for i in range(self.S):
            group_index = groups_assignment[i]
            self.shards_groups[group_index]["shard_index"].append(i)


        for i in range(self.K):
            amplitude = random.uniform(0, 1)
            offset_x = random.uniform(0, 2*math.pi)
            self.shards_groups[i]["amplitude"] = amplitude
            self.shards_groups[i]["offset_x"] = offset_x
            var = (amplitude * self.R)**2 

            for shard_index in self.shards_groups[i]["shard_index"]:
                self.vectors_amplitude[shard_index] = np.random.lognormal(mean=amplitude, sigma=math.sqrt(var))
        
            amplitude_group = [self.vectors_amplitude[shard_index] for shard_index in self.shards_groups[i]["shard_index"]]
            if (len(amplitude_group) == 0):
                print("Uwaga! Pewna grupa jest pusta. Najlepiej jakbyś dostosował parametry")
                continue
            kxres = self.calculate_KX(self.KI, amplitude_group)
            if kxres == None:
                return pd.DataFrame([])
            inside_group_offsets = kxres[0]
            
            for iiii in range(len(self.shards_groups[i]["shard_index"])):
                shard_index = self.shards_groups[i]["shard_index"][iiii]
                self.vectors_offset_x[shard_index] = inside_group_offsets[iiii]
                

        amplitudes = [self.shards_groups[i]["amplitude"] for i in range(self.K)]
        kxres = self.calculate_KX(self.KO, amplitudes)
        if kxres == None:
            return pd.DataFrame([])

        (offsets_between_groups, self.real_averaged_correlation) = kxres
        for i in range(self.K):
            group_offset = offsets_between_groups[i]
            for iiii in range(len(self.shards_groups[i]["shard_index"])):
                shard_index = self.shards_groups[i]["shard_index"][iiii]
                self.vectors_offset_x[shard_index] += group_offset

        
        highest_amplitude = 0
        for i in range(self.K):
            for shard_index in self.shards_groups[i]["shard_index"]:
                amplitude = self.vectors_amplitude[shard_index]
                highest_amplitude = max(highest_amplitude, amplitude)
        
        for i in range(self.K):
            for shard_index in self.shards_groups[i]["shard_index"]:
                load_vector:List[float] = [None] * self.dimensions
                amplitude = self.vectors_amplitude[shard_index]
                offset_x = self.vectors_offset_x[shard_index]

                for d in range(self.dimensions):
                    x = (2 * math.pi * self.CN * d) / self.dimensions
                    load_vector[d] = amplitude * math.sin(x + offset_x) + highest_amplitude
                self.list_of_load_vectors[shard_index] = load_vector
        return pd.DataFrame(self.list_of_load_vectors)

    def calculate_KX(self, kx, amplitude_list: List[float], n_points=500) -> List[float] | None:
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
        averaged_correlation = (np.sum(corr_matrix_opt) - n)/(n*n - n)
        print("Average correlation", averaged_correlation)
        print("KO DEBUG ==  END  == ")

        for i in range(len(corr_matrix_opt)):
            for j in range(len(corr_matrix_opt)):
                if i == j:
                    continue
                error = abs(kx - corr_matrix_opt[i, j])
                if error > self.kx_error_threshold:
                    return None

        return (best_offsets, averaged_correlation)

    def return_real_averaged_correlation(self):
        return self.real_averaged_correlation

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
    generator = ParametrizedGenerator(S=10, R=0.5, KO=0.7, CN=3, K=2, KI=1, dimensions=24, D=1.0)
    df = generator.generate()
    generator.print_results()
    print(df)