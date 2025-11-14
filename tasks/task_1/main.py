import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from generators.exp_random_generator import ExpRandomGenerator
from utils.node import Node
from utils.charts import ChartMSE
from algorithms.shard_algorithm import ShardAlgorithm
from algorithms.random_allocation import RandomAllocation
from algorithms.multiway_number_partitioning import MultiwayNumberPartitioning

if __name__ == "__main__":
    AVERAGE_SHARDS_PER_NODE = 10
    SHARD_COUNT = 54
    
    list_of_load_vectors = ExpRandomGenerator(
        shard_count=SHARD_COUNT,
        dimensions=24,
        lambda_value=1
    ).generate()

    node_count = round(SHARD_COUNT/AVERAGE_SHARDS_PER_NODE)
    nodes_random_allocation = [Node() for _ in range(node_count)]
    nodes_multiway_partitioning = [Node() for _ in range(node_count)]

    random_allocated = RandomAllocation(nodes_random_allocation)
    multiway_number_partitioning = MultiwayNumberPartitioning(nodes_multiway_partitioning)

    ALGORITHMS: list[ShardAlgorithm] = [random_allocated, multiway_number_partitioning]
    chart = ChartMSE()

    for a in ALGORITHMS:
        print("###############################################################")
        print("### Algorithm:", a.name, "###")
        a.allocate(list_of_load_vectors)

        # data_nodes = a.data_of_allocated_vectors()
        # for node in data_nodes:
            # print(node)

        score = a.algorithm_score()
        chart.add_series(a.name, score)
        print("Average MSE:", score["MSE_average"])
        print("Median MSE:", score["MSE_median"])
        print("Max MSE:", score["MSE_max"])
        print("\n")

    chart.draw()