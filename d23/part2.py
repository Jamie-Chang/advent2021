from __future__ import annotations
from itertools import chain, islice
from typing import Iterator, cast

from part1 import Amphipod, Position, State, minimise_cost, load


ADDITION = [
    "  #D#C#B#A#",
    "  #D#B#A#C#",
]


def read() -> Iterator[tuple[Position, Amphipod]]:
    with open("d23/input.txt") as f:
        lines = chain(
            islice(f, 1, 3),
            ADDITION,
            f,
        )
        for y, line in enumerate(lines):
            for x, c in enumerate(line[1:]):
                if c not in {"A", "B", "C", "D"}:
                    continue
                yield (x, y), cast(Amphipod, c)


if __name__ == "__main__":
    initial = load(read(), room_size=4)
    target = State(
        frozenset(
            [
                ((2, 1), "A"),
                ((2, 2), "A"),
                ((2, 3), "A"),
                ((2, 4), "A"),
                ((4, 1), "B"),
                ((4, 2), "B"),
                ((4, 3), "B"),
                ((4, 4), "B"),
                ((6, 1), "C"),
                ((6, 2), "C"),
                ((6, 3), "C"),
                ((6, 4), "C"),
                ((8, 1), "D"),
                ((8, 2), "D"),
                ((8, 3), "D"),
                ((8, 4), "D"),
            ]
        ),
        room_size=4,
    )
    print(minimise_cost(initial, target))
