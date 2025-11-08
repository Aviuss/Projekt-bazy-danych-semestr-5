# Usage:
# $ python exp_random_generator_run.py <shard_count> [filename]

# Examples:
# $ python exp_random_generator.py 30 result.txt
# $ python exp_random_generator.py 30

import sys
from exp_random_generator import ExpRandomGenerator

def main():
    
    if len(sys.argv) < 2:
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

    if len(sys.argv) >= 3 and sys.argv[2] != None:
        generator.print_result(sys.argv[2])     # save result to file
    else:
        generator.print_result()                # print result on console

main()
