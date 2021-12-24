from __future__ import annotations

from dataclasses import dataclass
from functools import cache, cached_property
from itertools import chain, product
from typing import Final, Iterator, Literal, TypeAlias


Position: TypeAlias = tuple[int, int]
Amphipod: TypeAlias = Literal["A", "B", "C", "D"]

DESTINATION: dict[Amphipod, int] = {"A": 2, "B": 4, "C": 6, "D": 8}
MOVE_COST: Final[dict[Amphipod, int]] = {"A": 1, "B": 10, "C": 100, "D": 1000}

HALLWAY_POSITIONS = {(0, 0), (1, 0), (3, 0), (5, 0), (7, 0), (9, 0), (10, 0)}
ROOM_POSITIONS = set(product(DESTINATION.values(), (0, 1)))


def _step(start: int, end: int) -> Iterator[int]:
    if end == start:
        return
    direction = 1 if end >= start else -1
    yield from range(start + direction, end + direction, direction)


def steps(start: Position, end: Position) -> Iterator[Position]:
    """
    >>> list(steps((2, 2), (4, 1)))
    [(2, 1), (2, 0), (3, 0), (4, 0), (4, 1)]
    >>> list(steps((2, 2), (2, 2)))
    []
    >>> list(steps((2, 1), (2, 2)))
    [(2, 2)]
    >>> list(steps((3, 0), (2, 2)))
    [(2, 0), (2, 1), (2, 2)]
    """
    match start, end:
        case (x0, 0), (x1, 0):
            return ((x, 0) for x in _step(x0, x1))
        case (x0, y0), (x1, y1) if x0 == x1:
            return ((x0, y) for y in _step(y0, y1))
        case (x0, y0), (x1, y1):
            return chain(
                steps((x0, y0), (x0, 0)),
                steps((x0, 0), (x1, 0)),
                steps((x1, 0), (x1, y1)),
            )
        case _:
            assert False, "Unhandled steps"


@dataclass(frozen=True)
class State:
    board: frozenset[tuple[Position, Amphipod]]
    room_size: int = 2

    @cached_property
    def positions(self) -> dict[Position, Amphipod]:
        return dict(self.board)

    def solved(self, position: Position):
        """
        >>> s = State(
        ...     board=frozenset(
        ...         {
        ...             ((4, 4), "D"),
        ...             ((7, 0), "B"),
        ...             ((5, 0), "B"),
        ...             ((1, 0), "C"),
        ...             ((8, 3), "C"),
        ...             ((8, 2), "A"),
        ...             ((0, 0), "D"),
        ...             ((3, 0), "D"),
        ...             ((9, 0), "B"),
        ...             ((4, 3), "B"),
        ...             ((8, 4), "A"),
        ...             ((6, 3), "A"),
        ...             ((6, 4), "C"),
        ...             ((2, 4), "A"),
        ...             ((4, 2), "C"),
        ...             ((8, 1), "D"),
        ...         }
        ...     ),
        ...     room_size=4,
        ... )
        >>> s.solved((2, 4))
        True
        """
        amphipod = self.positions[position]
        if position[0] != DESTINATION[amphipod]:
            return False
        return all(
            self.positions.get((DESTINATION[amphipod], y + 1)) == amphipod
            for y in range(position[1], self.room_size)
        )

    def solve(self, position: Position):
        amphipod = self.positions[position]
        destinations = ((DESTINATION[amphipod], y + 1) for y in range(self.room_size))
        candidate = None
        for p in destinations:
            value = self.positions.get(p)
            if value is None:
                candidate = p
                continue
            if value is not amphipod:
                return None
        return candidate

    def targets(self, start: Position):
        if self.solved(start):
            return {}

        target = self.solve(start)
        if target is not None:
            steps = self.steps(start, target)
            if steps is not None:
                return {target: steps}

        if start[1] == 0:
            return {}
        return {p: s for p in HALLWAY_POSITIONS if (s := self.steps(start, p))}

    def steps(self, start: Position, end: Position) -> int | None:
        total = 0
        for step in steps(start, end):
            if step in self.positions:
                return None
            total += 1

        return total

    def move(self, start: Position, end: Position) -> State:
        amphipod = self.positions[start]
        return State(
            (self.board | {(end, amphipod)}) - {(start, amphipod)},
            room_size=self.room_size,
        )

    def moves(self):
        for start, amphipod in self.board:
            for end, steps in self.targets(start).items():
                yield self.move(start, end), steps * MOVE_COST[amphipod]


@cache
def minimise_cost(state: State, target: State) -> int | None:
    if state == target:
        return 0

    return min(
        (
            step_cost + cost
            for s, step_cost in state.moves()
            if (cost := minimise_cost(s, target)) is not None
        ),
        default=None,
    )


if __name__ == "__main__":
    initial = State(
        frozenset(
            [
                ((2, 1), "B"),
                ((2, 2), "D"),
                ((4, 1), "A"),
                ((4, 2), "C"),
                ((6, 1), "A"),
                ((6, 2), "B"),
                ((8, 1), "D"),
                ((8, 2), "C"),
            ]
        )
    )
    target = State(
        frozenset(
            [
                ((2, 1), "A"),
                ((2, 2), "A"),
                ((4, 1), "B"),
                ((4, 2), "B"),
                ((6, 1), "C"),
                ((6, 2), "C"),
                ((8, 1), "D"),
                ((8, 2), "D"),
            ]
        )
    )
    print(minimise_cost(initial, target))
