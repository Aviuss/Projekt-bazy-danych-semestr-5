import sys

import pandas as pd
from pandas import DataFrame
from utils.input_output import InputOutput
from generators.exp_random_generator import ExpRandomGenerator
from utils.node import Node
from utils.charts import ChartMSE
from algorithms.random_allocation import RandomAllocation
from algorithms.multiway_number_partitioning import MultiwayNumberPartitioning
from algorithms.mean_squared_error_minimization import MeanSquaredErrorMinimization
from typing import List, Dict

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
        """
        Summary:
            Initializes the Main class with the specified mode and input file name.
        Parameters:
            mode(str): The mode of operation, either "generate" to create random load vectors or
                        "load" to read load vectors from a file.
            input_name(str): The name of the input file to read load vectors from (used only
                                when mode is "load").
        Returns:
            None
        """
        self.mode: str = mode
        self.input_name: str = input_name
        self.node_count: int = SHARD_COUNT // AVERAGE_SHARDS_PER_NODE
        self.chart: ChartMSE = ChartMSE()
        self.nodes: Dict[str, List[Node]] = {
            "random_allocation": [Node() for _ in range(self.node_count)],
            "multiway_partitioning": [Node() for _ in range(self.node_count)],
            "mean_squared_error_minimization": [Node() for _ in range(self.node_count)],
        }
        self.algorithms: dict[str, RandomAllocation | MultiwayNumberPartitioning] = {
            "random_allocation": RandomAllocation(self.nodes["random_allocation"]),
            "multiway_partitioning": MultiwayNumberPartitioning(self.nodes["multiway_partitioning"]),
            "mean_squared_error_minimization": MeanSquaredErrorMinimization(self.nodes["mean_squared_error_minimization"])
        }

    @staticmethod
    def generate_random_vectors() -> DataFrame:
        """
        Summary:
            Generates random load vectors using an exponential distribution.
        Parameters:
            None
        Returns:
            DataFrame: A DataFrame containing the generated load vectors.
        """
        return ExpRandomGenerator(
            shard_count=SHARD_COUNT,
            dimensions=DIMENSIONS,
            lambda_value=LAMBDA
        ).generate()

    def load_input_vectors(self, input_name: str) -> DataFrame:
        """
        Summary:
            Loads load vectors from a specified CSV file.
        Parameters:
            input_name(str): The name of the input file to read load vectors from.
        Returns:
            DataFrame: A DataFrame containing the loaded load vectors.
        """
        return self.read_input_file(input_name)

    def get_load_vectors(self) -> List:
        """
        Summary:
            Retrieves load vectors based on the specified mode (generate or load from file).
        Parameters:
            None
        Returns:
            List: A list of load vectors.
        """
        if self.mode == "generate":
            df_vectors: pd.DataFrame = self.generate_random_vectors()
        elif self.mode == "load":
            df_vectors: pd.DataFrame = self.load_input_vectors(self.input_name)
        else:
            raise Exception("Invalid mode:", self.mode)
        return df_vectors.values.tolist()

    def run_algorithms(self, list_of_load_vectors: list):
        """
        Summary:
            Runs each shard allocation algorithm on the provided load vectors and collects performance metrics.
        Parameters:
            list_of_load_vectors(list): A list of load vectors to be allocated by the algorithms.
        Returns:
            None
        """
        for algorithm_name, algorithm_obj in self.algorithms.items():
            print("###############################################################")
            print("### Algorithm:", algorithm_obj.name, "###")
            algorithm_obj.allocate(list_of_load_vectors)

            # data_nodes = a.data_of_allocated_vectors()
            # for node in data_nodes:
            # print(node)

            score: Dict[str, float] = algorithm_obj.algorithm_score()
            self.chart.add_series(algorithm_obj.name, score)
            print("Average MSE:", score["MSE_average"])
            print("Median MSE:", score["MSE_median"])
            print("Max MSE:", score["MSE_max"])
            print("###############################################################")
        self.chart.draw()

    def run(self):
        """
        Summary:
            Main execution method to get load vectors and run the shard allocation algorithms.
        Parameters:
            None
        Returns:
            None
        """
        list_load_vectors: List = self.get_load_vectors()
        self.run_algorithms(list_load_vectors)


if __name__ == "__main__":
    print(sys.argv[1], len((sys.argv)))
    if len(sys.argv) == 2 and sys.argv[1] == "generate":
        main: Main = Main(mode="generate")
        main.run()
    if len(sys.argv) == 3 and sys.argv[1] == "load":
        main: Main = Main(mode="load", input_name=sys.argv[2])
        main.run()
