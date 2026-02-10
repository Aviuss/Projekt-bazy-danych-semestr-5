import sys
import pandas as pd
from pandas import DataFrame
from utils.node import Node
from typing import List, Dict
import numpy as np

from algorithms.random_allocation import RandomAllocation
from algorithms.multiway_number_partitioning import MultiwayNumberPartitioning
from algorithms.mean_squared_error_minimization import MeanSquaredErrorMinimization
from algorithms.salp import ShardAllocationLoadPrediction
from algorithms.lsalp import LocalShardAllocationLoadPrediction
from generators.parametrized_generator import ParametrizedGenerator
import json
import matplotlib
matplotlib.use("TkAgg")

AVERAGE_SHARDS_PER_NODE = 10
SHARD_COUNT = 100


class Main():
    def __init__(self):
        self.node_count: int = SHARD_COUNT // AVERAGE_SHARDS_PER_NODE

    def init_methods(self):
        self.nodes: Dict[str, List[Node]] = {
            "random_allocation": [Node() for _ in range(self.node_count)],
            "multiway_partitioning": [Node() for _ in range(self.node_count)],
            "mean_squared_error_minimization": [Node() for _ in range(self.node_count)],
            "salp": [Node() for _ in range(self.node_count)],
            "lsalp": [Node() for _ in range(self.node_count)],
        }
        self.algorithms: dict = {
            "random_allocation": RandomAllocation(self.nodes["random_allocation"]),
            "multiway_partitioning": MultiwayNumberPartitioning(self.nodes["multiway_partitioning"]),
            "mean_squared_error_minimization": MeanSquaredErrorMinimization(self.nodes["mean_squared_error_minimization"]),
            "salp": ShardAllocationLoadPrediction(self.nodes["salp"]),
            "lsalp": LocalShardAllocationLoadPrediction(self.nodes["lsalp"]),
        }

    def run_algorithms(self, list_of_load_vectors: list):
        result = []
        for algorithm_name, algorithm_obj in self.algorithms.items():
            if algorithm_name == "lsalp":
                pre_allocator = ShardAllocationLoadPrediction(self.nodes["lsalp"])
                pre_allocator.allocate(list(list_of_load_vectors))
                
                algorithm_obj.allocate(error_threshold=0.1)
            else:
                algorithm_obj.allocate(list(list_of_load_vectors))

            score: Dict[str, float] = algorithm_obj.algorithm_score()            
            result.append((algorithm_name, score["MSE_average"]))
        return result

    def run(self):
        KO_array = np.linspace(0.5, 1, 100)
        
        results = []
        
        for KO in KO_array:
            self.init_methods()
            generator = ParametrizedGenerator(S=SHARD_COUNT, K=3, R=0.05, KO=KO, CN=1.0, D=2, KI=0.97, kx_error_threshold = 0.2)
            vectors = generator.generate()
            if vectors.empty:
                print("Couldn't fit KO or KI. Change parameters")
                continue
        
            results.append(
                {
                    "real_ko": generator.return_real_averaged_correlation(),
                    "mse_average": self.run_algorithms(vectors.to_numpy().tolist())
                }
            )
        file = open("results ko analysis.json", 'w+')
        file.write(json.dumps(results))
        file.close()

if __name__ == "__main__":
    main = Main()
    main.run()
