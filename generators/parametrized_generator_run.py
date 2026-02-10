# Usage:
# $ python parametrized_generator_run.py <shard_count> [filename]

# Examples:
# $ python parametrized_generator_run.py 30 result.csv
# $ python parametrized_generator_run.py 30

import sys
from parametrized_generator import ParametrizedGenerator


def main():
    if len(sys.argv) < 2:
        print("Missing required arguments")
        print("Usage: `python parametrized_generator_run.py <shard_count> [filename]`")
        return

    try:
        shard_count = int(sys.argv[1])
    except ValueError as e:
        print("Invalid argument shard_count:", e)
        return

    generator = ParametrizedGenerator(S=shard_count, K=3, R=0.05, KO=0.8, CN=1.0, D=3, KI=0.97, kx_error_threshold = 0.2)
    vectors = generator.generate()
    if vectors.empty:
        print("Couldn't fit KO or KI. Change parameters")
        return
    #generator.print_results()
    generator.create_plots()

    filename = sys.argv[2] if len(sys.argv) >= 3 else "result.csv"
    generator.save_to_csv_file(data=vectors, filename=filename)

main()
