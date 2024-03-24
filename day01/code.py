import os
import sys
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file

if __name__ == "__main__":
    # Input
    calibration_input_lines = from_file.get_input_for(1)
    if calibration_input_lines == None:
        sys.exit(1)

    # Part One
    def find_first_numeric(line: str, reverse: bool = False) -> str:
        n = len(line)
        start, stop, step = 0, n, 1
        if reverse:
            start, stop, step = n - 1, -1, -1
        for i in range(start, stop, step):
            if line[i].isnumeric():
                return line[i]
        return ""

    try:
        sum = 0
        for line in calibration_input_lines:
            if line == "":
                continue
            bch = find_first_numeric(line=line)
            ech = find_first_numeric(line=line, reverse=True)
            sum += int(bch + ech)
        print(f"[Part 1] ans = {sum}")
    except Exception as e:
        print(f"[Part 1] exception = ${e}")

    # Part Two
    replacement_map = {
        3: {
            "one": "1",
            "two": "2",
            "six": "6",
        },
        4: {
            "four": "4",
            "five": "5",
            "nine": "9",
        },
        5: {
            "three": "3",
            "seven": "7",
            "eight": "8",
        },
    }

    def find_first_numeric_advanced(line: str, reverse=False) -> str:
        n = len(line)
        start, stop, step = 0, n, 1
        if reverse:
            start, stop, step = n - 1, -1, -1
        for i in range(start, stop, step):
            if line[i].isnumeric():
                return line[i]
            for rc, rm in replacement_map.items():
                to_check: Optional[str] = None
                if not reverse and i + rc <= n:
                    to_check = line[i : i + rc]
                elif reverse and i - rc + 1 >= 0:
                    to_check = line[i - rc + 1 : i + 1]
                if to_check != None and to_check in rm:
                    return rm[to_check]
        return ""

    try:
        sum = 0
        for line in calibration_input_lines:
            if line == "":
                continue
            bch = find_first_numeric_advanced(line=line)
            ech = find_first_numeric_advanced(line=line, reverse=True)
            sum += int(bch + ech)
        print(f"[Part 2] ans = {sum}")
    except Exception as e:
        print(f"[Part 2] exception = ${e}")
