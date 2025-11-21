import random
from algorithms.shard_algorithm import ShardAlgorithm

class MultiwayNumberPartitioning(ShardAlgorithm):
    def __init__(self, list_of_nodes):
        super().__init__("Multiway number partitioning", list_of_nodes)

    def allocate(self, list_of_load_vectors):
        if len(list_of_load_vectors) == 0:
            return

        list_of_load_vectors.sort(
            key = lambda listx: max(
                abs(max(listx)),
                abs(min(listx))
            ), # sort by maximum norm
            reverse=True
        ) # sort from largest to smallest
        
        dim = len(list_of_load_vectors[0])

        for examined_vector in list_of_load_vectors:
            nodes_len = len(self.list_of_nodes)
            vector_sum_with_examined_vector = [
                self.add_vectors(
                    self.list_of_nodes[i].vector_sum_of_load_vectors(if_null_default_dimention=dim),
                    examined_vector
                )
                for i in range(nodes_len)
            ]
            maximum_norm_for_vectsum_w_examvect = [
                max(
                    abs(max(vector_sum_with_examined_vector[i])),
                    abs(min(vector_sum_with_examined_vector[i]))
                )
                for i in range(nodes_len)
            ]

            min_maxnorm = {
                "min_value": None,
                "list_of_node_indexes": []
            }

            for i in range(nodes_len):
                isSet = min_maxnorm["min_value"] != None
                isEqual = isSet and maximum_norm_for_vectsum_w_examvect[i] == min_maxnorm["min_value"]
                isSmaller = isSet and maximum_norm_for_vectsum_w_examvect[i] < min_maxnorm["min_value"]
                
                if  isSmaller or not isSet:
                    min_maxnorm["min_value"] = maximum_norm_for_vectsum_w_examvect[i]
                    min_maxnorm["list_of_node_indexes"] = [i]
                elif isEqual:
                    min_maxnorm["list_of_node_indexes"].append(i)
            
            if min_maxnorm["min_value"] == None:
                raise Exception("Sth went horribly wrong, probably nodes_len is not set")

            selected_node_idx = None
            if len(min_maxnorm["list_of_node_indexes"]) == 1:
                selected_node_idx = min_maxnorm["list_of_node_indexes"][0]
            else:
                random_uniform_choice = random.randint(0, len(min_maxnorm["list_of_node_indexes"]) - 1)
                selected_node_idx = min_maxnorm["list_of_node_indexes"][random_uniform_choice]

            self.list_of_nodes[selected_node_idx].add_load_vector(examined_vector)
            self.visualize_allocation()

    def add_vectors(self, a, b):
        K = len(a)
        if K != len(b):
            raise Exception("Can't add vectors with different dimentions")
        
        sum_vector = [0 for _ in range(K)]
        for k in range(K):
            sum_vector[k] += a[k]
            sum_vector[k] += b[k]

        return sum_vector