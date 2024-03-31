import os
import re
import sys
from dataclasses import dataclass
from typing import List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file


@dataclass
class ScratchCard:
    winning_numbers: List[int]
    collected_numbers: List[int]
    copies = 1

    def matches(self) -> int:
        n = 0
        for w in self.winning_numbers:
            for c in self.collected_numbers:
                if w == c:
                    n += 1
        return n

    def increase_copy(self, n: int) -> None:
        self.copies += n


if __name__ == "__main__":
    # Input
    scratchcards_input = from_file.get_input_for(4)
    if scratchcards_input == None:
        sys.exit(1)

    # Parse Input
    all_cards: List[ScratchCard] = []
    for line in scratchcards_input:
        m = re.match(r"Card\s+\d+: ([\s\d]+) \| ([\s\d]+)", line)
        if m == None:
            print(f"could not match line {line}, exiting")
            sys.exit(1)
        all_cards.append(
            ScratchCard(
                winning_numbers=[int(n) for n in m.group(1).strip().split()],
                collected_numbers=[int(n) for n in m.group(2).strip().split()],
            )
        )

    # Part One
    points_sum = 0
    for card in all_cards:
        matches = card.matches()
        if matches > 0:
            points_sum += pow(2, matches - 1)

    print(f"[Part 1] ans = {points_sum}")

    # Part Two
    total_cards = 0
    i = 0
    n = len(all_cards)
    while i < n:
        card = all_cards[i]
        i += 1
        total_cards += card.copies
        matches = card.matches()
        if matches == 0:
            continue
        j = i
        while matches > 0 and j < n:
            all_cards[j].increase_copy(n=card.copies)
            j += 1
            matches -= 1

    print(f"[Part 2] ans = {total_cards}")
