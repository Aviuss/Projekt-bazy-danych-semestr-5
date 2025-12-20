import numpy as np

class VectorsUtils:
    @staticmethod
    def sum_vectors(vectors: list[list[float]]) -> list[float]:
        arr = np.array(vectors)
        summed_vector = np.sum(arr ** 2, axis=0)
        return summed_vector.tolist()


    @staticmethod
    def angle_between_vectors(A: np.ndarray, B: np.ndarray) -> tuple[float, float]:
        dot_product = np.dot(A, B)
        norm_A = np.linalg.norm(A)
        norm_B = np.linalg.norm(B)
        cos_angle = dot_product / (norm_A * norm_B)
        radians = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        degrees = np.degrees(radians)
        return radians, degrees