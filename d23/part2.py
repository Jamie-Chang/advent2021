from __future__ import annotations

from part1 import State, minimise_cost


if __name__ == "__main__":
    initial = State(
        frozenset(
            [
                ((2, 1), "B"),
                ((2, 2), "D"),
                ((2, 3), "D"),
                ((2, 4), "D"),
                ((4, 1), "A"),
                ((4, 2), "C"),
                ((4, 3), "B"),
                ((4, 4), "C"),
                ((6, 1), "A"),
                ((6, 2), "B"),
                ((6, 3), "A"),
                ((6, 4), "B"),
                ((8, 1), "D"),
                ((8, 2), "A"),
                ((8, 3), "C"),
                ((8, 4), "C"),
            ]
        ),
        room_size=4,
    )

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
