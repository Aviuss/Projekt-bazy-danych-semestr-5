# Usage:
# $ python exp_random_generator_run.py <shard_count> [filename]

# Examples:
# $ python exp_random_generator_run.py 30 result.txt
# $ python exp_random_generator_run.py 30

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
    vectors = generator.generate()
    generator.print_results()

    filename = sys.argv[2] if len(sys.argv) >= 3 else "result.csv"
    generator.save_to_csv_file(data=vectors, filename=filename)

main()
