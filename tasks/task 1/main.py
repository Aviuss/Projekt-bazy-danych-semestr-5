import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from generators.primitive_generator import Primitive_generator

if __name__ == "__main__":
    generator = Primitive_generator(shard_count=10)
    generator_results = generator.generate()
    print(generator_results)