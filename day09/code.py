import os
import sys
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file

if __name__ == "__main__":
    # Input
    input_lines = from_file.get_input_for(9)
    if input_lines == None:
        sys.exit(1)

    # Parse Input
    historical_values: List[List[int]] = []
    for line in input_lines:
        historical_values.append([int(s) for s in line.split()])

    # Part One
    def extrapolate_last_value(
        values: List[int],
    ) -> int:
        n = len(values)
        if n == 0:
            return 0
        v = values[-1]
        if all([v == i for i in values[1:]]):
            return v
        values_diff = [values[i + 1] - values[i] for i in range(n - 1)]
        return v + extrapolate_last_value(values=values_diff)

    values_sum = 0
    for sequence in historical_values:
        values_sum += extrapolate_last_value(values=sequence)
    print(f"[Part 1] ans = {values_sum}")

    # Part Two
    def extrapolate_first_value(
        values: List[int],
    ) -> int:
        n = len(values)
        if n == 0:
            return 0
        v = values[0]
        if all([v == i for i in values[1:]]):
            return v
        values_diff = [values[i + 1] - values[i] for i in range(n - 1)]
        return v - extrapolate_first_value(values=values_diff)

    values_sum = 0
    for sequence in historical_values:
        values_sum += extrapolate_first_value(values=sequence)
    print(f"[Part 2] ans = {values_sum}")
