import numpy as np
import random
from algorithms.shard_algorithm import ShardAlgorithm
from utils.vectors_utils import VectorFactory

class ShardAllocationLoadPrediction(ShardAlgorithm):
    def __init__(self, list_of_nodes):
        super().__init__("SALP", list_of_nodes)
        self.vector_factory = VectorFactory()
    
    def allocate(self, list_of_load_vectors):
        WTSObjects = self.vector_factory.get_wts_sum(list_of_load_vectors)
        self.vector_factory.sort_vector_objects(WTSObjects, reverse=True)
        
        LW = [np.array(x.load_vector) for x in WTSObjects]
        N = len(self.list_of_nodes)

        total_system_load = np.sum(LW, axis=0)
        NWTS = total_system_load / N

        FS = [[] for _ in range(N)]
        WS = [np.zeros_like(NWTS) for _ in range(N)]
        CV = [np.abs(np.zeros_like(NWTS) - NWTS) for _ in range(N)]

        for i in range(len(LW)):
            F_i = LW[i]
            max_SAM = float('-inf')
            max_j = []

            for j in range(N):
                alfa_CVi_before = self.vector_factory.angle_between_vectors(CV[j], NWTS)
                CVi_before = self.vector_factory.vector_norm(CV[j])

                WS_copy = WS[j] + F_i
                CV_copy = np.abs(WS_copy - NWTS)

                alfa_CVi_after = self.vector_factory.angle_between_vectors(CV_copy, NWTS)
                CVi_after = self.vector_factory.vector_norm(CV_copy)

                delta_alfa_CVi = alfa_CVi_after - alfa_CVi_before
                delta_CVi = CVi_before - CVi_after
                
                nwts_norm = self.vector_factory.vector_norm(NWTS)
                
                if nwts_norm == 0:
                    SAM = 0
                else:
                    SAM = ((delta_alfa_CVi + 90.0) / 180.0) * delta_CVi / nwts_norm

                if SAM > max_SAM:
                    max_SAM = SAM
                    max_j = [j]
                elif SAM == max_SAM:
                    max_j.append(j)
                    
            node_idx = random.choice(max_j)
            self.list_of_nodes[node_idx].add_load_vector(LW[i])

            FS[node_idx].append(F_i)
            WS[node_idx] = WS[node_idx] + F_i
            CV[node_idx] = np.abs(WS[node_idx] - NWTS)
            self.visualize_allocation()