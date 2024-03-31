import os
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file


@dataclass
class PartNumber:
    row_number: int
    start_indx: int
    end_indx: int
    value: int

    def __hash__(self) -> int:
        return self.row_number + self.start_indx + self.end_indx

    def in_vicinity(self, indx: Tuple[int, int]) -> bool:
        if self.row_number < indx[0] - 1 or self.row_number > indx[0] + 1:
            return False
        if indx[1] < self.start_indx - 1 or indx[1] > self.end_indx + 1:
            return False
        return True


if __name__ == "__main__":
    # Input
    engine_lines = from_file.get_input_for(3)
    if engine_lines == None:
        sys.exit(1)

    # Parse Input
    all_parts: List[PartNumber] = []
    for i, line in enumerate(engine_lines):
        num_buf: str = ""
        num_start: Optional[int] = None
        num_end: Optional[int] = None
        for j, c in enumerate(line):
            if c.isdigit():
                if num_buf == "":
                    num_start = j
                num_buf += c
                num_end = j
            elif num_buf != "":
                all_parts.append(
                    PartNumber(
                        row_number=i,
                        start_indx=num_start,
                        end_indx=num_end,
                        value=int(num_buf),
                    )
                )
                num_start, num_end, num_buf = None, None, ""
        if num_buf != "":
            all_parts.append(
                PartNumber(
                    row_number=i,
                    start_indx=num_start,
                    end_indx=num_end,
                    value=int(num_buf),
                )
            )

    # Part One
    part_numbers_sum = 0
    addable: List[PartNumber] = []
    for i, line in enumerate(engine_lines):
        for j, c in enumerate(line):
            if c.isdigit() or c == ".":
                continue
            # This is a special character
            for p in all_parts:
                if not p.in_vicinity(indx=(i, j)):
                    continue
                if p not in addable:
                    addable.append(p)
                    part_numbers_sum += p.value

    print(f"[Part 1] ans = {part_numbers_sum}")

    # Part Two
    gear_ratios_sum = 0
    for i, line in enumerate(engine_lines):
        for j, c in enumerate(line):
            if c != "*":
                continue
            # This could be a gear
            gear_parts: List[PartNumber] = []
            for p in all_parts:
                if not p.in_vicinity(indx=(i, j)):
                    continue
                gear_parts.append(p)
                if len(gear_parts) > 2:
                    # This cannot be a gear
                    break
            else:
                if len(gear_parts) == 2:
                    gear_ratios_sum += gear_parts[0].value * gear_parts[1].value

    print(f"[Part 2] ans = {gear_ratios_sum}")
