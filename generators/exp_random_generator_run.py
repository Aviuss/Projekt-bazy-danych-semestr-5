# Usage:
# $ python exp_random_generator_run.py <shard_count> [filename]

# Examples:
# $ python exp_random_generator_run.py 30 result.txt
# $ python exp_random_generator_run.py 30

import sys
import os
from exp_random_generator import ExpRandomGenerator

def main():
    
    if len(sys.argv) < 3:
        print("Missing required arguments")
        print("Usage: `python exp_random_generator_run.py <shard_count> [filename]`")
        return

    try:
        shard_count = int(sys.argv[1])
    except ValueError as e:
        print("Invalid argument shard_count:", e)
        return
    
    generator = ExpRandomGenerator(shard_count)
    generator.generate()
    generator.print_results()      

    if 'vectors_data' not in os.listdir('../'):
        os.mkdir('../vectors_data')
        generator.save_results('../vectors_data/' + sys.argv[2])
    else:
        generator.save_results('../vectors_data/' + sys.argv[2])   

main()
