import sys
import pandas as pd
from pandas import DataFrame
from utils.input_output import InputOutput
from generators.exp_random_generator import ExpRandomGenerator
from utils.node import Node
from utils.charts import ChartMSE
from typing import List, Dict

from algorithms.random_allocation import RandomAllocation
from algorithms.multiway_number_partitioning import MultiwayNumberPartitioning
from algorithms.mean_squared_error_minimization import MeanSquaredErrorMinimization
from algorithms.salp import ShardAllocationLoadPrediction
from algorithms.lsalp import LocalShardAllocationLoadPrediction

AVERAGE_SHARDS_PER_NODE = 10
SHARD_COUNT = 54
DIMENSIONS = 24
LAMBDA = 1


class Main(InputOutput):
    """
    The main class to run different shard allocation algorithms and compare their performance.
    It can either generate random load vectors or load them from a CSV file.
    """

    def __init__(self, mode: str = "generate", input_name: str = "input_vectors.csv"):
        self.mode: str = mode
        self.input_name: str = input_name
        self.node_count: int = SHARD_COUNT // AVERAGE_SHARDS_PER_NODE
        self.chart: ChartMSE = ChartMSE()
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

    @staticmethod
    def generate_random_vectors() -> DataFrame:
        return ExpRandomGenerator(
            shard_count=SHARD_COUNT,
            dimensions=DIMENSIONS,
            lambda_value=LAMBDA
        ).generate()

    def load_input_vectors(self, input_name: str) -> DataFrame:
        return self.read_input_file(input_name)

    def get_load_vectors(self) -> List:
        if self.mode == "generate":
            df_vectors: pd.DataFrame = self.generate_random_vectors()
        elif self.mode == "load":
            df_vectors: pd.DataFrame = self.load_input_vectors(self.input_name)
        else:
            raise Exception("Invalid mode:", self.mode)
        return df_vectors.values.tolist()

    def run_algorithms(self, list_of_load_vectors: list):
        for algorithm_name, algorithm_obj in self.algorithms.items():
            print("###############################################################")
            print("### Algorithm:", algorithm_obj.name, "###")
            
            if algorithm_name == "lsalp":
                pre_allocator = ShardAllocationLoadPrediction(self.nodes["lsalp"])
                pre_allocator.allocate(list(list_of_load_vectors))
                
                algorithm_obj.allocate(error_threshold=0.1)
            else:
                algorithm_obj.allocate(list(list_of_load_vectors))

            score: Dict[str, float] = algorithm_obj.algorithm_score()
            self.chart.add_series(algorithm_obj.name, score)
            
            try:
                algorithm_obj.create_gif(fps=4)
            except Exception:
                pass

            print("Average MSE:", score["MSE_average"])
            print("Median MSE:", score["MSE_median"])
            print("Max MSE:", score["MSE_max"])
            print("###############################################################")
        
        self.chart.draw()

    def run(self):
        list_load_vectors: List = self.get_load_vectors()
        self.run_algorithms(list_load_vectors)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "generate":
        main: Main = Main(mode="generate")
        main.run()
    elif len(sys.argv) == 3 and sys.argv[1] == "load":
        main: Main = Main(mode="load", input_name=sys.argv[2])
        main.run()
    else:
        main: Main = Main(mode="generate")
        main.run()