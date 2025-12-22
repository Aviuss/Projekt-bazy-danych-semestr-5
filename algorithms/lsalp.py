import numpy as np
import copy
from algorithms.salp import ShardAllocationLoadPrediction
from algorithms.shard_algorithm import ShardAlgorithm
from utils.mean_squared_error import MeanSquaredError

class LocalShardAllocationLoadPrediction(ShardAlgorithm):
    def __init__(self, list_of_nodes):
        super().__init__("LSALP", list_of_nodes)
        self.mse_calculator = MeanSquaredError(self.list_of_nodes)

    def _get_global_average_vector(self):
        total_load = np.zeros(24)
        for node in self.list_of_nodes:
            total_load += np.array(node.vector_sum_of_load_vectors())
        return total_load / len(self.list_of_nodes)

    def allocate(self, error_threshold: float, max_iterations: int = 50):
        NWTS = self._get_global_average_vector()
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            mse_result = self.mse_calculator.calc_MSE()
            current_avg_mse = mse_result["average"]
            nodes_mse_list = mse_result["nodes_MSE"]

            if current_avg_mse <= error_threshold:
                return True

            max_mse_value = max(nodes_mse_list)
            max_node_index = nodes_mse_list.index(max_mse_value)
            node_max = self.list_of_nodes[max_node_index]

            best_partner = None
            min_pair_error = float("inf")
            
            node_max_load = np.array(node_max.vector_sum_of_load_vectors())
            target_pair_load = 2 * NWTS

            for node in self.list_of_nodes:
                if node is node_max:
                    continue

                node_load = np.array(node.vector_sum_of_load_vectors())
                combined_load = node_max_load + node_load
                
                pair_mse = np.mean((combined_load - target_pair_load) ** 2)

                if pair_mse < min_pair_error:
                    min_pair_error = pair_mse
                    best_partner = node

            if best_partner is None:
                return False

            old_shards_max = list(node_max.list_of_load_vectors)
            old_shards_partner = list(best_partner.list_of_load_vectors)

            local_shards = old_shards_max + old_shards_partner

            node_max.list_of_load_vectors = []
            best_partner.list_of_load_vectors = []

            local_salp = ShardAllocationLoadPrediction([node_max, best_partner])
            local_salp.allocate(local_shards)

            new_mse_result = self.mse_calculator.calc_MSE()
            new_avg_mse = new_mse_result["average"]

            if new_avg_mse < current_avg_mse:
                continue
            else:
                node_max.list_of_load_vectors = old_shards_max
                best_partner.list_of_load_vectors = old_shards_partner
                return False
        return True