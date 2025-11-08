import random
from utils.node import Node
import numpy as np

class Random_allocation:
    def __init__(self, list_of_nodes):
        self.list_of_nodes = list_of_nodes

    def allocate(self, list_of_load_vectors):
        for load_vector in list_of_load_vectors:
            random_uniform_choice = random.randint(0, len(self.list_of_nodes) - 1)
            self.list_of_nodes[random_uniform_choice].add_load_vector(load_vector)
        return
     
    def data_of_allocated_vectors(self):
        data = []
        for index, node in enumerate(self.list_of_nodes):
            node_data = {
                "node": index,
                "load_vector_count": len(node.list_of_load_vectors),
                "average": np.mean(node.list_of_load_vectors),
                "sum": np.sum(node.list_of_load_vectors)
            }
            data.append(node_data)
        return data
