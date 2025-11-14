import numpy as np
from typing import Dict
from utils.node import Node
import utils.mean_squared_error as mse

# The parent (abstract) class "ShardAlgorithm" for other algorithms
class ShardAlgorithm:
    def __init__(self, name: str, list_of_nodes: list[Node]):
        self.name = name
        self.list_of_nodes = list_of_nodes

    # Allocates shards to nodes, sets 
    def allocate(self, _list_of_load_vectors):
        pass
    
    def data_of_allocated_vectors(self) -> list[Dict[str, float]]:
        data = []
        for index, node in enumerate(self.list_of_nodes):
            node_data = {
                "node": index,
                "load_vector_count": len(node.list_of_load_vectors),
                "average": np.mean(node.list_of_load_vectors),
                "median": np.median(node.list_of_load_vectors),
                "sum": np.sum(node.list_of_load_vectors),
            }
            data.append(node_data)
        return data
    
    def algorithm_score(self) -> Dict[str, float]:
        MSE_result = mse.MeanSquaredError(self.list_of_nodes).calc_MSE()
        score = {
            "MSE_average": MSE_result["average"],
            "MSE_median": MSE_result["median"],
            "MSE_max": MSE_result["max"]
        }
        return score
