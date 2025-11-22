from __future__ import annotations
from typing import Dict, Iterator, TypeVar
from algorithms.shard_algorithm import ShardAlgorithm
from utils.node import Node
from utils.mean_squared_error import MeanSquaredError
from copy import deepcopy, copy
import random
from dataclasses import dataclass
from typing import List


@dataclass
class L2Object:
    """Class to represent an object with L2 norm information."""
    index: int = None
    sum: int | float = None
    load_vector: list[float] = None


@dataclass
class DeltaObject:
    """Class to represent an object with delta information."""
    index: int = None
    delta: int | float = None
    sum: int | float = None


@dataclass
class DeltaNode:
    """Class to represent a collection of DeltaObjects."""
    delta_list: List[DeltaObject]

    def __iter__(self) -> Iterator[DeltaObject]:
        """Iterator over the delta_list."""
        return iter(self.delta_list)

    def __len__(self) -> int:
        """Returns the number of DeltaObjects in the delta_list."""
        return len(self.delta_list)

    def get_best_delta(self, sorting=False) -> DeltaObject:
        """
        Summary:
            Retrieves the DeltaObject with the highest delta value. If sorting is True, sorts the delta_list first.
        Parameters:
            self: The DeltaNode instance.
            sorting (bool): If True, sorts the delta_list before retrieving the best delta.
        Returns:
            DeltaObject
        """
        if sorting:
            return max(self.delta_list, key=lambda x: (x.delta, -x.sum))
        return self.delta_list[0]  # use that after sorting

    def sort(self) -> None:
        """
        Summary:
            Sorts the delta_list in place based on delta (descending) and sum (ascending).
        Parameters:
            self: The DeltaNode instance.
        Returns:
            None
        """
        self.delta_list.sort(key=lambda x: (x.delta, -x.sum), reverse=True)

    def find_delta_objects_by_sum_and_delta(self, sum_value: int | float, delta_value: int | float) -> DeltaNode | None:
        """
        Summary:
            Finds DeltaObjects in the delta_list that match the specified sum and delta values.
        Parameters:
            self: The DeltaNode instance.
            sum_value (int | float): The sum value to match.
            delta_value (int | float): The delta value to match.
        Returns:
            DeltaNode | None - A DeltaNode containing matching DeltaObjects or None if no matches are found.
        """
        delta = [d for d in self.delta_list if d.sum == sum_value and d.delta == delta_value]
        if len(delta) == 0:
            return None
        return DeltaNode(delta_list=delta)

    def has_duplicate_best_result(self) -> bool:
        """
        Summary:
            Checks if there are multiple DeltaObjects in the delta_list with the same best delta and sum
        Parameters:
            self: The DeltaNode instance.
        Returns:
            bool - True if duplicates exist, False otherwise.
        """
        best_delta = self.get_best_delta()
        count = sum(1 for delta in self.delta_list if delta.delta == best_delta.delta and delta.sum == best_delta.sum)
        return count > 1

    def append(self, delta_object: DeltaObject) -> None:
        """
        Summary:
            Appends a DeltaObject to the delta_list.
        Parameters:
            self: The DeltaNode instance.
            delta_object(DeltaObject): The DeltaObject to append.
        Returns:
            None
        """
        self.delta_list.append(delta_object)


def sort_L2Objects(list_of_L2Objects: List[L2Object]) -> None:
    """
    Summary:
        Sorts a list of L2Objects in place based on their sum attribute in descending order
    Parameters:
        list_of_L2Objects (List[l2Object]): The list of L2Objects to sort.
    Returns:
        None
    """
    list_of_L2Objects.sort(key=lambda x: x.sum, reverse=True)


class MeanSquaredErrorMinimization(ShardAlgorithm):
    """Class implementing the Mean Squared Error Minimization algorithm."""

    def __init__(self, list_of_nodes: list[Node]):
        super().__init__("Mean squared error minimization", list_of_nodes)

    @staticmethod
    def sum_squared_load_vector(list_of_load_vectors: list[list[float]]) -> List[L2Object]:
        """
        Summary:
            Calculates the sum of squares for each load vector and returns a list of L2Objects.
        Parameters:
            list_of_load_vectors (list[list[float]]): A list of load vectors.
        Returns:
            List[L2Object]: A list of L2Objects containing index, sum of squares, and the load vector itself.
        """
        L2: List[L2Object] = [
            L2Object(
                index=index,
                sum=sum(x ** 2 for x in vector),
                load_vector=vector
            )
            for index, vector in enumerate(list_of_load_vectors)
        ]
        return L2

    def allocate(self, list_of_load_vectors: list[list[float]]):
        """
        Summary:
            Allocates load vectors to nodes in a way that minimizes the mean squared error.
        Parameters:
            list_of_load_vectors (list[list[float]]): A list of load vectors to allocate.
        Returns:
            None
        """
        L2: List[L2Object] = self.sum_squared_load_vector(list_of_load_vectors)
        sort_L2Objects(L2)

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
