import math
import numpy as np
from typing import List
from .dataobjects import L2Object, VectorObject,WTSObject


class VectorsUtils:
    @staticmethod
    def _sum_squared_load_vector(list_of_load_vectors: List[List[float]],output_type: WTSObject | L2Object) -> List[VectorObject]:
        """
        Summary:
            Calculates the sum of squares for each load vector and returns a List of VectorObject.
        Parameters:
            list_of_load_vectors (List[List[float]]): A List of load vectors.
        Returns:
            List[WTSObject | L2Object]: A List of VectorObject containing index, sum of squares, and the load vector itself.
        """
        vector_obj: List[WTSObject| L2Object] = [
            output_type(
                index=index,
                sum=sum(x ** 2 for x in vector),
                load_vector=vector
            )
            for index, vector in enumerate(list_of_load_vectors)
        ]
        return vector_obj
    
    @staticmethod
    def _sum_load_vector(list_of_load_vectors: List[List[float]],output_type : WTSObject | L2Object) -> WTSObject| L2Object:
        """
        Summary:
            Calculates the sum for each load vector and returns a List of VectorObject.
        Parameters:
            list_of_load_vectors (List[List[float]]): A List of load vectors.
        Returns:
            List[WTSObject | L2Object]: A List of VectorObject containing index, sum, and the load vector itself.
        """
        
        vector_obj: List[WTSObject| L2Object] = [
            output_type(
                index=index,
                sum=sum(x for x in vector),
                load_vector=vector
            )
            for index, vector in enumerate(list_of_load_vectors)
        ]

        return vector_obj


class VectorCalculations:
    @staticmethod
    def vector_norm(vector: np.ndarray) -> float:
        s = 0
        for x in vector:
            s += x**2
        
        return math.sqrt(s)

    @staticmethod
    def angle_between_vectors(A: np.ndarray, B: np.ndarray) -> tuple[float, float]:
        dot_product = np.dot(A, B)
        norm_A = np.linalg.norm(A)
        norm_B = np.linalg.norm(B)

        if norm_A == 0 or norm_B == 0:
            return 0, 0

        cos_angle = dot_product / (norm_A * norm_B)
        radians = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        degrees = np.degrees(radians)
        return degrees
    



class VectorFactory(VectorsUtils,VectorCalculations):

    def get_l2_squared(self,list_of_load_vectors: List[List[float]]) -> List[L2Object]:
        """L2Object shortcut"""
        return self._sum_squared_load_vector(list_of_load_vectors, L2Object)

    def get_wts_squared(self,list_of_load_vectors: List[List[float]]) -> List[WTSObject]:
        """WTSObject shortcut"""
        return self._sum_squared_load_vector(list_of_load_vectors, WTSObject)

    def get_wts_sum(self,list_of_load_vectors: List[List[float]]) -> WTSObject:
        """WTSObject shortcut for sum"""
        return self._sum_load_vector(list_of_load_vectors,WTSObject)

    def get_l2_sum(self,list_of_load_vectors: List[List[float]]) -> List[L2Object]:
        """L2Object shortcut for sum"""
        return self._sum_load_vector(list_of_load_vectors,L2Object)
    

    
    @staticmethod
    def sort_vector_objects(vector_objects: List[WTSObject| L2Object], reverse: bool = True) -> List[WTSObject| L2Object]:
        """
        Summary:
            Sorts a list of VectorObject based on their sum attribute.
        Parameters:
            vector_objects (List[WTSObject | L2Object]): A List of VectorObject to be sorted.
            descending (bool): If True, sorts in descending order; otherwise, in ascending order.
        Returns:
            List[WTSObject | L2Object]: A sorted List of VectorObject.
        """
        return sorted(vector_objects, key=lambda obj: obj.sum, reverse=reverse)



