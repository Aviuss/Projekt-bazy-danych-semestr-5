class Node:
    def __init__(self):
        self.list_of_load_vectors = []

    def add_load_vector(self, load_vector):
        self.list_of_load_vectors.append(load_vector)

    def vector_sum_of_load_vectors(self, if_null_default_dimention = None):
        if len(self.list_of_load_vectors) == 0:
            if if_null_default_dimention == None:
                return []
            else:
                return [0 for _ in range(if_null_default_dimention)]

        K = len(self.list_of_load_vectors[0])
        sum_vector = [0 for _ in range(K)]
        for vector in self.list_of_load_vectors:
            for k in range(K):
                sum_vector[k] += vector[k]
    
        return sum_vector

        