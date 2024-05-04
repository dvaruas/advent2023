from __future__ import annotations

import os
import re
import sys
from math import lcm
from typing import List, Set, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from utils import from_file


class Node:
    s: str
    left: Node
    right: Node

    def __init__(self, s) -> None:
        self.s = s

    def __hash__(self) -> int:
        return hash(self.s)

    def __str__(self) -> str:
        return self.s


if __name__ == "__main__":
    # Input
    input_lines = from_file.get_input_for(8)
    if input_lines == None:
        sys.exit(1)

    # Parse Input
    movement_instructions = input_lines[0]
    nodes: dict[str, Node] = {}
    for line in input_lines[2:]:
        m = re.match(r"(\w+) = \((\w+), (\w+)\)", line)
        for i in range(1, 4):
            if m.group(i) not in nodes:
                nodes[m.group(i)] = Node(m.group(i))
        n, nl, nr = nodes[m.group(1)], nodes[m.group(2)], nodes[m.group(3)]
        n.left = nl
        n.right = nr

    def find_steps(
        node: Node,
        end_condition: callable[Node, bool],
    ) -> Tuple[int, Node]:
        steps = 0
        i, n = 0, len(movement_instructions)
        while not end_condition(node):
            if movement_instructions[i] == "L":
                node = node.left
            else:
                node = node.right
            i += 1
            if i == n:
                i = 0
            steps += 1
        return (steps, node)

    # Part One
    steps, _ = find_steps(
        node=nodes["AAA"],
        end_condition=lambda n: n.s == "ZZZ",
    )
    print(f"[Part 1] ans = {steps}")

    # Part Two
    all_steps: Set[int] = set()
    starting_nodes = [nodes[n] for n in nodes if n.endswith("A")]
    for node in starting_nodes:
        visited_endings: List[Node] = []
        while True:
            steps, end_node = find_steps(
                node=node,
                end_condition=lambda n: n.s.endswith("Z"),
            )
            all_steps.add(steps)

            if end_node in visited_endings:
                break

            visited_endings.append(end_node)

    print(f"[Part 2] ans = {lcm(*all_steps)}")
