from dataclasses import dataclass
from typing import Iterator, List, TypeVar

DeltaNode = TypeVar('DeltaNode')



@dataclass
class VectorObject:
    """Class to represent an object with L2 norm information."""
    index: int = None
    sum: int | float = None
    load_vector: list[float] = None

@dataclass
class WTSObject(VectorObject):
    """Class to represent an object with WTS norm information."""


    def sort_by_load_vector(self) -> None:
        """
        Summary:
            Sorts the load_vector in descending order.
        Parameters:
            self: The WTSObject instance.
        Returns:
            None
        """
        if self.load_vector is not None:
            self.load_vector.sort(reverse=True)


@dataclass
class L2Object(VectorObject):
    """Class to represent an object with L2 norm information."""

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

