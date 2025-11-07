import random

class Random_allocation:
    def __init__(self, list_of_nodes):
        self.list_of_nodes = list_of_nodes

    def allocate(self, list_of_load_vectors):
        for load_vector in list_of_load_vectors:
            random_uniform_choice = random.randint(0, len(self.list_of_nodes) - 1)
            self.list_of_nodes[random_uniform_choice].add_load_vector(load_vector)
        return 