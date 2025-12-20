import numpy as np
from algorithms.shard_algorithm import ShardAlgorithm
from utils.vectors_utils import VectorFactory, VectorFactory
import random

class ShardAllocationLoadPrediction(ShardAlgorithm):
    def __init__(self, list_of_nodes):
        super().__init__("SALP", list_of_nodes)
        self.vector_factory = VectorFactory()
    
    def allocate(self, list_of_load_vectors):

        WTSObjects = self.vector_factory.get_wts_sum(list_of_load_vectors)
        WTS: list[float] = [x.sum for x in WTSObjects]

        N: int = len(self.list_of_nodes)
        NWTS: list[float] = [(1/N)*x for x in WTS]

        FS: list[list[list[float]]] = []    # shards
        WS: list[list[float]] = []          # load vector
        CV: list[list[float]] = []          # difference
        self.vector_factory.sort_vector_objects(WTSObjects, reverse=True)
        LW: list[list[float]] = [x.load_vector for x in WTSObjects]


        for i in range(N):
            FS.append([])
            WS.append([0] * 24)
            CV.append(NWTS.copy())


        for i in range(len(LW)):
            F_i:list[float]  = LW[i]
            max_SAM = float('-inf')
            max_j: list[int] = []


            for j in range(len(FS)):

                # alfa_CVi_before & alfa_CVi_after --> in degrees
                alfa_CVi_before = self.vector_factory.angle_between_vectors(CV[j], NWTS)
                CVi_before = self.vector_factory.vector_norm(CV[j])

                FS_copy = FS[j].copy()
                WS_copy = WS[j].copy()
                CV_copy = CV[j].copy()

                FS_copy.append(F_i)
                WS_copy = np.sum([WS_copy, F_i], axis=0)
                CV_copy = [abs(x - y) for x, y in zip(WS_copy, NWTS)]


                alfa_CVi_after = self.vector_factory.angle_between_vectors(CV_copy, NWTS)
                CVi_after = self.vector_factory.vector_norm(CV_copy)


                delta_alfa_CVi = alfa_CVi_after - alfa_CVi_before  # degrees
                delta_CVi = CVi_before - CVi_after      # ?? before - after
                SAM = ((delta_alfa_CVi + 90.0) / 180.0) * delta_CVi / self.vector_factory.vector_norm(NWTS)

                if SAM > max_SAM:
                    max_SAM = SAM
                    max_j = [j]
                elif SAM == max_SAM:
                    max_j.append(j)
                    
            node = random.choice(max_j)
            self.list_of_nodes[node].add_load_vector(LW[i])

            FS[max_j].append(F_i)
            WS[max_j] = np.sum([WS[max_j], F_i], axis=0) # vectors sum
            CV[max_j] = [abs(x - y) for x, y in zip(WS[i], NWTS)]

