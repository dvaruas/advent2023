import os
import re
import sys
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file

if __name__ == "__main__":
    # Input
    game_lines = from_file.get_input_for(2)
    if game_lines == None:
        sys.exit(1)

    # Parse input
    game_plays: dict[int, List[dict[str, int]]] = {}
    for line in game_lines:
        m = re.match(r"Game (\d+): (.+)", line)
        g_num = int(m.group(1))
        game_plays[g_num] = []
        parts = m.group(2).split(";")
        for p in parts:
            found_red, found_green, found_blue = 0, 0, 0
            for in_p in p.split(","):
                m = re.match(r"(\d+) (\w+)", in_p.strip())
                ball_count = int(m.group(1))
                match m.group(2):
                    case "red":
                        found_red += ball_count
                    case "blue":
                        found_blue += ball_count
                    case "green":
                        found_green += ball_count
                    case _:
                        print("something is wrong here")
                        sys.exit(1)
            parts_d = {"r": found_red, "g": found_green, "b": found_blue}
            game_plays[g_num].append(parts_d)

    # Part One
    given_red, given_green, given_blue = 12, 13, 14
    possible_games_sum = 0
    for g_num, g_list in game_plays.items():
        for g_dict in g_list:
            found_red = g_dict["r"]
            found_green = g_dict["g"]
            found_blue = g_dict["b"]
            if (
                found_red > given_red
                or found_blue > given_blue
                or found_green > given_green
            ):
                break
        else:
            possible_games_sum += g_num
    print(f"[Part 1] ans = {possible_games_sum}")

    # Part Two
    power_sum = 0
    for g_num, g_list in game_plays.items():
        min_red, min_green, min_blue = 0, 0, 0
        for g_dict in g_list:
            found_red = g_dict["r"]
            found_green = g_dict["g"]
            found_blue = g_dict["b"]
            min_red = max(min_red, found_red)
            min_green = max(min_green, found_green)
            min_blue = max(min_blue, found_blue)
        power_sum += min_red * min_green * min_blue
    print(f"[Part 2] ans = {power_sum}")
