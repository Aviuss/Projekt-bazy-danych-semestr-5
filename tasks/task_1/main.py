import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from generators.exp_random_generator import ExpRandomGenerator
from utils.node import Node
from shard_allocation_algorithms.random_allocation import Random_allocation
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
    list_of_nodes = [Node() for _ in range(node_count)]

    # Random_allocation(
    #     list_of_nodes = list_of_nodes
    # ).allocate(
    #     list_of_load_vectors = list_of_load_vectors
    # )
    # data = Random_allocation(list_of_nodes).data_of_allocated_vectors()
    
    random_allocated = Random_allocation(list_of_nodes)
    random_allocated.allocate(list_of_load_vectors)
    data_random_allocated = random_allocated.data_of_allocated_vectors()
    
    for _ in data_random_allocated:
        print(_)
