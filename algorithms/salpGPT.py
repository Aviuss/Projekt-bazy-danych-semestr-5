import numpy as np
import random
from algorithms.shard_algorithm import ShardAlgorithm
import math

class ShardAlocationLoadPrediction(ShardAlgorithm):
    def __init__(self, list_of_nodes):
        super().__init__("SALP", list_of_nodes)
        self.nodes = list_of_nodes

    def _norm(self, v):
        return np.linalg.norm(v)

    def _angle(self, v1, v2):
        n1 = self._norm(v1)
        n2 = self._norm(v2)
        if n1 == 0 or n2 == 0:
            return 0.0
        cos_val = np.dot(v1, v2) / (n1 * n2)
        cos_val = np.clip(cos_val, -1.0, 1.0)
        return math.degrees(math.acos(cos_val))

    def allocate(self, list_of_load_vectors):
        num_nodes = len(self.nodes)
        T = len(list_of_load_vectors[0])

        # --- 1. Obliczenie WTS i NWTS ---
        WTS = np.zeros(T)
        for w in list_of_load_vectors:
            WTS += np.array(w)

        NWTS = WTS / num_nodes
        NWTS_norm = self._norm(NWTS)

        # --- 2. Sortowanie shardów wg normy malejąco ---
        sorted_load_vectors = sorted(
            list_of_load_vectors,
            key=lambda v: self._norm(v),
            reverse=True
        )

        # --- 3. Inicjalizacja węzłów ---
        for node in self.nodes:
            node.list_of_load_vectors = []

        # --- 4. Główna pętla SALP ---
        for shard_vector in sorted_load_vectors:
            shard_vector = np.array(shard_vector)

            best_sam = -float("inf")
            best_nodes = []

            for node in self.nodes:
                # stan przed
                TWS_before = np.array(
                    node.vector_sum_of_load_vectors(if_null_default_dimention=T)
                )
                CV_before = NWTS - TWS_before
                alpha_before = self._angle(CV_before, NWTS)
                norm_before = self._norm(CV_before)

                # stan po
                TWS_after = TWS_before + shard_vector
                CV_after = NWTS - TWS_after
                alpha_after = self._angle(CV_after, NWTS)
                norm_after = self._norm(CV_after)

                # składniki SAM
                delta_alpha = alpha_after - alpha_before
                delta_norm = norm_before - norm_after

                SAM = ((delta_alpha + 90.0) / 180.0) * (delta_norm / NWTS_norm)

                if SAM > best_sam:
                    best_sam = SAM
                    best_nodes = [node]
                elif SAM == best_sam:
                    best_nodes.append(node)

            # --- losowanie przy remisie ---
            chosen_node = random.choice(best_nodes)
            chosen_node.add_load_vector(shard_vector.tolist())


#if __name__ == "__main__":
#    gen = ExpRandomGenerator(20)
#    gen.generate()
#    list_of_load_vectors = gen.list_of_load_vectors
#
#    NODES_LEN = 10
#    list_of_nodes = []
#    for i in range(NODES_LEN):
#        list_of_nodes.append(Node())
#
#    alg = ShardAlocationLoadPrediction(list_of_nodes)
#    alg.allocate(list_of_load_vectors)
#
#    print("end")