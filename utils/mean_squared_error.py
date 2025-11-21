import numpy as np
from utils.node import Node

# returns { average, median, max } MSE (mean squared error) of all nodes
class MeanSquaredError:

    def __init__(self, nodes_all: list[Node]):
        self.nodes_all = nodes_all

    def set_nodes_all(self, nodes_all: list[Node]):
        self.nodes_all = nodes_all

    def calc_MSE(self):
        NODES = len(self.nodes_all)
        HOURS = 24
        sum_all = [0] * HOURS
        average_all = [None] * HOURS
        nodes_sums = []
        nodes_MSE = []

        for node in self.nodes_all:
            sum_current_node = [0] * HOURS

            for vector in node.list_of_load_vectors:
                for i in range(HOURS):
                    sum_current_node[i] += vector[i]
                    sum_all[i] += vector[i]
            nodes_sums.append(sum_current_node)

        for i in range(HOURS):
            average_all[i] = sum_all[i] / NODES
        
        for node_sum in nodes_sums:
            mean_squared_error = 0

            for i in range(HOURS):
                diff = node_sum[i] - average_all[i]
                mean_squared_error += diff ** 2

            mean_squared_error /= 24
            nodes_MSE.append(mean_squared_error)

        result = {
            "average": np.mean(nodes_MSE),
            "median": np.median(nodes_MSE),
            "max": max(nodes_MSE),
            "nodes_MSE": nodes_MSE
        }
        return result