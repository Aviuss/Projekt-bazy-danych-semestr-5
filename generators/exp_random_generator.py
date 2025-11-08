import math
import random

class ExpRandomGenerator:
    def __init__(self, shard_count, dimensions = 24, lambda_value = 1):
        self.list_of_load_vectors = [None] * shard_count
        self.shard_count = shard_count
        self.lambda_value = lambda_value
        self.dimensions = dimensions

    def generate(self):
        for i in range(self.shard_count):
            self.list_of_load_vectors[i] = [None] * self.dimensions
            for j in range(self.dimensions):
                self.list_of_load_vectors[i][j] = random.expovariate(self.lambda_value)
        return self.list_of_load_vectors

    def print_result(self, filename=None):
        result = ""
        for i in range(len(self.list_of_load_vectors)):
            for j in range(len(self.list_of_load_vectors[i])):
                result += str(self.list_of_load_vectors[i][j])
                
                if j < len(self.list_of_load_vectors[i]) - 1:
                    result += " " 
        
            result += "\n"
        
        if (filename):
            file = open(filename, "w")
            file.write(result)
            file.close()
            print("Result saved to:", filename)
        else:
            print(result)
        
        return
