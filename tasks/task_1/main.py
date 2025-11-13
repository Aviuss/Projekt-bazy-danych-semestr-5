import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from generators.exp_random_generator import ExpRandomGenerator
from utils.node import Node
from shard_allocation_algorithms.random_allocation import Random_allocation
from shard_allocation_algorithms.Multidimentional_Multiway_Number_Partitioning import Multidimentional_Multiway_Number_Partitioning
import math

if __name__ == "__main__":
    AVERAGE_SHARDS_PER_NODE = 10
    SHARD_COUNT = 54
    
    list_of_load_vectors = ExpRandomGenerator(
        shard_count=SHARD_COUNT,
        dimensions=24,
        lambda_value=1
    ).generate()

    node_count = round(SHARD_COUNT/AVERAGE_SHARDS_PER_NODE)
    list_of_nodes_for_random_allocation = [Node() for _ in range(node_count)]
    list_of_nodes_for_multiway_partitioning = [Node() for _ in range(node_count)]

    random_allocated = Random_allocation(list_of_nodes_for_random_allocation)
    random_allocated.allocate(list_of_load_vectors)
    data_random_allocated = random_allocated.data_of_allocated_vectors()
    
    multiway_number_partitioning = Multidimentional_Multiway_Number_Partitioning(list_of_nodes_for_multiway_partitioning)
    multiway_number_partitioning.allocate(list_of_load_vectors)
    data_multiway_allocated = multiway_number_partitioning.data_of_allocated_vectors()

    print("\n## Data random allocated")
    for _ in data_random_allocated:
        print(_)
    
    print("\n## Data multiway allocated")
    for _ in data_multiway_allocated:
        print(_)
    print("\n")