from __future__ import annotations
from typing import Dict, Iterator, TypeVar
from algorithms.shard_algorithm import ShardAlgorithm
from utils.node import Node
from utils.mean_squared_error import MeanSquaredError
from copy import deepcopy, copy
import random
from dataclasses import dataclass
from typing import List
from utils.dataobjects import DeltaObject, DeltaNode, L2Object
from utils.vectors_utils import VectorFactory


class MeanSquaredErrorMinimization(ShardAlgorithm):
    """Class implementing the Mean Squared Error Minimization algorithm."""

    def __init__(self, list_of_nodes: list[Node]):
        super().__init__("Mean squared error minimization", list_of_nodes)
        self.vector_factory: VectorFactory = VectorFactory()

    def allocate(self, list_of_load_vectors: list[list[float]]):
        """
        Summary:
            Allocates load vectors to nodes in a way that minimizes the mean squared error.
        Parameters:
            list_of_load_vectors (list[list[float]]): A list of load vectors to allocate.
        Returns:
            None
        """
        L2: List[L2Object] = self.vector_factory.get_l2_squared(list_of_load_vectors=list_of_load_vectors)
        self.vector_factory.sort_vector_objects(vector_objects=L2, reverse=True)

        for L2_vector in L2:
            delta_node: DeltaNode = DeltaNode([])
            self.calculate_delta_impacts(L2_vector=L2_vector, delta_node=delta_node)
            delta_node.sort()

            best_delta: DeltaObject = delta_node.get_best_delta()
            if delta_node.has_duplicate_best_result():
                max_deltas: DeltaNode = delta_node.find_delta_objects_by_sum_and_delta(sum_value=best_delta.sum,
                                                                                       delta_value=best_delta.delta)
                best_delta: DeltaObject = random.choice(max_deltas.delta_list)

            self.list_of_nodes[best_delta.index].add_load_vector(L2_vector.load_vector)
            self.visualize_allocation()
        return

    def calculate_delta_impacts(self, L2_vector: L2Object, delta_node: DeltaNode) -> None:
        """
        Summary:
            Calculates the impact of adding a load vector to each node in terms of mean squared error reduction
        Parameters:
            L2_vector (L2Object): The load vector to evaluate.
            delta_node (DeltaNode): The DeltaNode to store the results.
        Returns:
            None
        """
        mse_calculator: MeanSquaredError = MeanSquaredError(self.list_of_nodes)
        nodes_MSE: List = mse_calculator.calc_MSE().get("nodes_MSE")
        for index, node in enumerate(self.list_of_nodes):
            mse_before: int = nodes_MSE[index]

            nodes_simulation: List[Node] = copy(self.list_of_nodes)
            active_node_copy: Node = deepcopy(node)

            active_node_copy.add_load_vector(L2_vector.load_vector)
            nodes_simulation[index] = active_node_copy

            mse_calculator.set_nodes_all(nodes_simulation)
            mse_results: List[int | float] = mse_calculator.calc_MSE().get("nodes_MSE")
            mse_after: int | float = mse_results[index]

            current_total_load: int = sum(sum(vec) for vec in node.list_of_load_vectors)

            delta_node.append(DeltaObject(
                index=index,
                delta=mse_before - mse_after,
                sum=current_total_load
            ))
