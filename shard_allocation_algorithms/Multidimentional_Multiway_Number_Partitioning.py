import random
import numpy as np

class Multidimentional_Multiway_Number_Partitioning:
    def __init__(self, list_of_nodes):
        self.list_of_nodes = list_of_nodes

    def allocate(self, list_of_load_vectors):
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
