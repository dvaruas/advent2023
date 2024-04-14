import os
import re
import sys
from typing import List, Optional, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file


class MatchMap:
    ranges: List[Tuple[Tuple[int, int], Tuple[int, int]]]

    def __init__(self, map_lines: List[str]) -> None:
        self.ranges = []
        for line in map_lines:
            digits = re.findall(r"\d+", line)
            if len(digits) != 3:
                print(
                    "something went wrong while parsing map line, "
                    "could not find expected 3 digits : {line}"
                )
                sys.exit(1)
            digits = [int(d) for d in digits]
            self.ranges.append(
                (
                    (digits[1], digits[1] + digits[2]),
                    (digits[0], digits[0] + digits[2]),
                )
            )

    def __str__(self) -> str:
        return "Matches: " + " | ".join([f"{r[0]} -> {r[1]}" for r in self.ranges])

    def get_destination(self, source: int) -> int:
        for r_source, r_dest in self.ranges:
            r_source_start, r_source_end = r_source
            r_dest_start, _ = r_dest
            if r_source_start <= source < r_source_end:
                return r_dest_start + (source - r_source_start)
        return source

    def get_destination_ranges(
        self, source_ranges: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        destination_ranges: List[Tuple[int, int]] = []
        while len(source_ranges) > 0:
            sr_start, sr_end = source_ranges.pop()
            for r_source, r_dest in self.ranges:
                r_source_start, r_source_end = r_source
                r_dest_start, _ = r_dest
                overlap_start = max(sr_start, r_source_start)
                overlap_end = min(sr_end, r_source_end)
                if overlap_start >= overlap_end:
                    continue
                destination_ranges.append(
                    (
                        r_dest_start + overlap_start - r_source_start,
                        r_dest_start + overlap_end - r_source_start,
                    )
                )
                if overlap_start > sr_start:
                    source_ranges.append((sr_start, overlap_start))
                if overlap_end < sr_end:
                    source_ranges.append((overlap_end, sr_end))
                break
            else:
                destination_ranges.append((sr_start, sr_end))
        return destination_ranges


if __name__ == "__main__":
    # Input
    almanac_lines = from_file.get_input_for(5)
    if almanac_lines == None:
        sys.exit(1)

    # Parse Input
    i, n = 0, len(almanac_lines)
    seed_inputs: List[int] = []
    maps: List[MatchMap] = []
    map_lines: List[MatchMap] = []
    while i < n:
        line = almanac_lines[i].strip()
        if line == "":
            if len(map_lines) > 0:
                maps.append(MatchMap(map_lines=map_lines))
                map_lines = []

        elif line.startswith("seeds:"):
            # seeds line
            seed_inputs = [int(s) for s in re.findall(r"\d+", line)]
            if len(seed_inputs) == 0:
                print(f"something went wrong while parsing seeds line : {line}")
                sys.exit(1)

        elif line[0].isdigit():
            # map line
            map_lines.append(line)

        i += 1

    if len(map_lines) > 0:
        maps.append(MatchMap(map_lines=map_lines))

    # Part One
    lowest: Optional[int] = None
    for seed in seed_inputs:
        destination = seed
        for m in maps:
            destination = m.get_destination(source=destination)
        if lowest == None or lowest > destination:
            lowest = destination

    print(f"[Part 1] ans = {lowest}")

    # Part Two
    source_range: List[Tuple[int, int]] = []
    for i in range(0, len(seed_inputs), 2):
        source_range.append((seed_inputs[i], seed_inputs[i] + seed_inputs[i + 1]))
    for m in maps:
        source_range = m.get_destination_ranges(source_ranges=source_range)

    lowest = sorted(source_range, key=lambda x: x[0])[0][0]
    print(f"[Part 2] ans = {lowest}")
