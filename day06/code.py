import os
import re
import sys
from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file

if __name__ == "__main__":
    # Input
    input_lines = from_file.get_input_for(6)
    if input_lines == None:
        sys.exit(1)

    # Parse Input
    times = re.findall(r"\d+", input_lines[0])
    distances = re.findall(r"\d+", input_lines[1])

    def total_winning_ways(t: int, d: int) -> int:
        i = 1
        while i < t:
            d_i = (t - i) * i
            if d_i > d:
                return t - (2 * i) + 1
            i += 1
        raise ValueError(f"incorrect time={t} or distance={d}")

    # Part One
    result = reduce(
        lambda r, pair: r * total_winning_ways(t=int(pair[0]), d=int(pair[1])),
        zip(times, distances),
        1,
    )
    print(f"[Part 1] ans = {result}")

    # Part Two
    t = int("".join(times))
    d = int("".join(distances))
    result = total_winning_ways(t=t, d=d)
    print(f"[Part 2] ans = {result}")
