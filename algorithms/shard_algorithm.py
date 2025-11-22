import numpy as np
from typing import Dict
from utils.node import Node
import utils.mean_squared_error as mse
import os
import matplotlib.pyplot as plt

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
    
    def visualize_allocation(self):
        if 'graphs' not in os.listdir():
            os.mkdir('graphs')
        if './graphs/' + self.name.replace(" ", "_") + '_graph.png' in os.listdir('./graphs/'):
            os.remove('./graphs/' + self.name.replace(" ", "_") + '_graph.png')
        plt.clf()
        node_numbers = list(range(len(self.list_of_nodes)))
        loaded_vectors_sum = [node_data['sum'] for node_data in self.data_of_allocated_vectors()]
        
        bars = plt.bar(node_numbers, loaded_vectors_sum)

        for bar in bars:
            h = round(bar.get_height())
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                h,
                str(h),
                ha='center',
                va='bottom'
            )

        plt.ion()
        plt.bar(node_numbers, loaded_vectors_sum)
        plt.xlabel('Node Index')
        plt.ylabel('Sum of Load Vectors')
        plt.title(f'Load Vector Allocation using {self.name}')
        plt.xticks(node_numbers)
        plt.show()
        plt.pause(0.1)
        plt.savefig('./graphs/' + self.name.replace(" ", "_") + '_graph.png')
        plt.ioff()
        
        return
