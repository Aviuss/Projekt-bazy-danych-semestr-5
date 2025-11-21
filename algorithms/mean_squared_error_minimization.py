from typing import Dict
from algorithms.shard_algorithm import ShardAlgorithm
from utils.node import Node
from utils.mean_squared_error import MeanSquaredError
import random


class MeanSquaredErrorMinimization(ShardAlgorithm):
    def __init__(self, list_of_nodes: list[Node]):
        super().__init__("Mean squared error minimization", list_of_nodes)

    def allocate(self, list_of_load_vectors: list[list[float]]):

        L2: list[Dict[str, int | float]] = []

        for index, load_vector in enumerate(list_of_load_vectors):
            vector_sum = 0
            for i in range(len(load_vector)):
                vector_sum += load_vector[i] ** 2

            L2.append({"index": index, "sum": vector_sum, "load_vector": load_vector})
        L2.sort(key=lambda x: x["sum"], reverse=True)
        # print(L2)

        for L2_vector in L2:
            deltas = []
            MSE = MeanSquaredError(self.list_of_nodes)
            nodes_MSE = MSE.calc_MSE().get("nodes_MSE")

            for index, node in enumerate(self.list_of_nodes):
                MSE_before = nodes_MSE[index]

                list_of_nodes_copy = self.list_of_nodes.copy()
                list_of_nodes_copy[index].add_load_vector(L2_vector["load_vector"])
                MSE.set_nodes_all(list_of_nodes_copy)
                MSE_after = MSE.calc_MSE().get("nodes_MSE")[index]

                deltas.append(
                    {"index": index, "delta": MSE_after - MSE_before, "sum": sum(node.list_of_load_vectors[0])})

            deltas.sort(key=lambda x: (x["delta"], -x["sum"]), reverse=True)

            if deltas[0]["delta"] == deltas[1]["delta"] and deltas[0]["sum"] == deltas[1]["sum"]:
                max_delta = deltas[0]["delta"]
                max_sum = deltas[0]["sum"]
                max_deltas = [x for x in deltas if x["delta"] == max_delta and x["sum"] == max_sum]
                d = random.choice(max_deltas)
            else:
                d = deltas[0]

            self.list_of_nodes[d["index"]].add_load_vector(L2_vector["load_vector"])
            print(self.data_of_allocated_vectors())

        return
