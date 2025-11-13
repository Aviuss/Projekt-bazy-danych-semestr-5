# Usage:
# $ python exp_random_generator_run.py <shard_count> [filename]

# Examples:
# $ python exp_random_generator_run.py 30 result.txt
# $ python exp_random_generator_run.py 30

import sys
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
    generator.save_results(sys.argv[2])   

main()
