from __future__ import annotations

import os
import sys
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file


def get_cards_count(
    cards: List[str],
    joker_edition: bool,
) -> dict[str, int]:
    card_count: dict[str, int] = {}
    for c in cards:
        card_count[c] = card_count.get(c, 0) + 1
    if joker_edition:
        j_count = card_count.pop("J", 0)
        if j_count != 0:
            if len(card_count) == 0:
                # means it had only jokers in it.
                card_count["J"] = j_count
            else:
                max_key = max(card_count, key=lambda x: card_count[x])
                card_count[max_key] += j_count
    return card_count


def compare_hands_lt(
    this_hand: CardHand,
    other_hand: CardHand,
    joker_edition: bool,
) -> int:
    if this_hand.hand_type != other_hand.hand_type:
        return this_hand.hand_type < other_hand.hand_type

    def determine_card_number(card: str) -> int:
        if card.isnumeric():
            return int(card)
        if joker_edition and card == "J":
            # in the joker edition, 'J' has the least value among all.
            # so anything less than 2 is okay to be returned from here.
            return 1
        non_numeric_cards = ["A", "K", "Q", "J", "T"]
        i = non_numeric_cards.index(card)
        if i == -1:
            raise ValueError(f"incorrect card {card}")
        return 9 + 5 - i

    for c1, c2 in zip(this_hand.cards, other_hand.cards):
        n_c1, n_c2 = determine_card_number(card=c1), determine_card_number(card=c2)
        if n_c1 == n_c2:
            continue
        return n_c1 < n_c2


class HandType(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7

    def __lt__(self, other: HandType) -> bool:
        return self.value > other.value

    @staticmethod
    def from_card_count(card_count: dict[str, int]) -> HandType:
        distinct_cards = sorted(list(card_count.keys()), key=lambda x: card_count[x])
        match len(distinct_cards):
            case 1:
                return HandType.FIVE_OF_A_KIND
            case 2:
                dc_0, dc_1 = distinct_cards
                if card_count[dc_0] == 1 and card_count[dc_1] == 4:
                    return HandType.FOUR_OF_A_KIND
                elif card_count[dc_0] == 2 and card_count[dc_1] == 3:
                    return HandType.FULL_HOUSE
            case 3:
                dc_0, dc_1, dc_2 = distinct_cards
                if (
                    card_count[dc_0] == 1
                    and card_count[dc_1] == 1
                    and card_count[dc_2] == 3
                ):
                    return HandType.THREE_OF_A_KIND
                if (
                    card_count[dc_0] == 1
                    and card_count[dc_1] == 2
                    and card_count[dc_2] == 2
                ):
                    return HandType.TWO_PAIR
            case 4:
                return HandType.ONE_PAIR
            case 5:
                return HandType.HIGH_CARD


class CardHand(ABC):
    cards: List[str]
    hand_type: HandType

    def __init__(self, input_str: str) -> None:
        self.cards = []

        i, n = 0, len(input_str)
        while i < n:
            ch = input_str[i]
            self.cards.append(ch)
            i += 1

        self.hand_type = self.get_hand_type()

    @classmethod
    @abstractmethod
    def get_hand_type(self) -> HandType:
        pass

    def __str__(self) -> str:
        return f'Hand: {"".join(self.cards)}'


class RegularCardHand(CardHand):
    def get_hand_type(self) -> HandType:
        return HandType.from_card_count(
            get_cards_count(
                self.cards,
                joker_edition=False,
            )
        )

    def __lt__(self, other: RegularCardHand) -> bool:
        return compare_hands_lt(
            this_hand=self,
            other_hand=other,
            joker_edition=False,
        )


class JokerCardHand(CardHand):
    def get_hand_type(self) -> HandType:
        return HandType.from_card_count(
            get_cards_count(
                self.cards,
                joker_edition=True,
            )
        )

    def __lt__(self, other: JokerCardHand) -> bool:
        return compare_hands_lt(
            this_hand=self,
            other_hand=other,
            joker_edition=True,
        )


if __name__ == "__main__":
    # Input
    input_lines = from_file.get_input_for(7)
    if input_lines == None:
        sys.exit(1)

    # Part One
    game: List[Tuple[RegularCardHand, int]] = []
    for line in input_lines:
        card_input, bid_input = line.split()
        game.append((RegularCardHand(card_input), int(bid_input)))

    game = sorted(game, key=lambda x: x[0])
    result = 0
    for i, g in enumerate(game, start=1):
        result += i * g[1]
    print(f"[Part 1] ans = {result}")

    # Part Two
    game: List[Tuple[JokerCardHand, int]] = []
    for line in input_lines:
        card_input, bid_input = line.split()
        game.append((JokerCardHand(card_input), int(bid_input)))

    game = sorted(game, key=lambda x: x[0])
    result = 0
    for i, g in enumerate(game, start=1):
        result += i * g[1]
    print(f"[Part 2] ans = {result}")
