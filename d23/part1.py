from __future__ import annotations

from dataclasses import dataclass
from functools import cache, cached_property
from itertools import islice
from typing import Final, Iterator, Literal, TypeAlias, cast


Position: TypeAlias = tuple[int, int]
Amphipod: TypeAlias = Literal["A", "B", "C", "D"]

DESTINATION: dict[Amphipod, int] = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}
MOVE_COST: Final[dict[Amphipod, int]] = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

HALLWAY_SPOTS: Final[set[Position]] = {
    (0, 0),
    (1, 0),
    (3, 0),
    (5, 0),
    (7, 0),
    (9, 0),
    (10, 0),
}


@dataclass(frozen=True)
class State:
    board: frozenset[tuple[Position, Amphipod]]
    room_size: int = 2

    @cached_property
    def positions(self) -> dict[Position, Amphipod]:
        return dict(self.board)

    def __contains__(self, key: Position):
        return key in self.positions

    @cached_property
    def rooms(self):
        return {a: RoomView(x, self) for a, x in DESTINATION.items()}

    @cached_property
    def hallway(self):
        return HallwayView(self)

    def move(self, start: Position, end: Position) -> tuple[State, int]:
        # print(f"move: {start} -> {end}")
        amphipod = self.positions[start]
        return (
            State(
                (self.board | {(end, amphipod)}) - {(start, amphipod)},
                room_size=self.room_size,
            ),
            steps_between(start, end) * MOVE_COST[amphipod],
        )

    def move_out(self, room: RoomView):
        p, amphipod = room[-1]

        for spot in self.hallway.empty_spots():
            if self.hallway.blocked(spot[0], room.x):
                continue

            yield self.move(p, spot)

        target_room = self.rooms[amphipod]
        if target_room is room:
            return

        if self.hallway.blocked(target_room.x, room.x):
            return

        if target_room.evictable():
            return

        yield self.move(p, target_room.next_spot())

    def move_in(self):
        for spot, amphipod in self.hallway:
            target = self.rooms[amphipod]
            if target.evictable():
                continue

            if self.hallway.blocked(spot[0], target.x):
                continue

            yield self.move(spot, target.next_spot())

    def moves(self):
        for room in self.rooms.values():
            if room.solved():
                continue

            if not room.evictable():
                continue

            yield from self.move_out(room)

        yield from self.move_in()


@dataclass
class RoomView:
    x: int
    state: State

    @property
    def size(self) -> int:
        return self.state.room_size

    @property
    def target(self) -> Amphipod:
        match self.x:
            case 2:
                return "A"
            case 4:
                return "B"
            case 6:
                return "C"
            case 8:
                return "D"
            case _:
                assert False

    def _translate(self, y: int) -> Position:
        if y < 0:
            y = len(self) + y
        return self.x, self.size - y

    def __getitem__(self, y: int):
        return (p := self._translate(y)), self.state.positions[p]

    def __iter__(self):
        for y in range(self.size):
            p = self._translate(y)
            if p not in self.state:
                return
            yield self[y]

    def __len__(self):
        length = 0
        for y in range(1, 1 + self.size):
            if (self.x, y) not in self.state:
                continue
            length += 1
        return length

    def next_spot(self) -> Position:
        return self._translate(len(self))

    def evictable(self) -> bool:
        for _, a in self:
            if a != self.target:
                return True
        return False

    def houseable(self) -> bool:
        return not (self.solved() or self.evictable())

    def solved(self) -> bool:
        return not self.evictable() and len(self) == self.size


@dataclass
class HallwayView:
    state: State

    def _translate(self, x: int) -> Position:
        return x, 0

    def __getitem__(self, x: int):
        return self.state.positions[self._translate(x)]

    def empty_spots(self) -> Iterator[Position]:
        return (p for p in HALLWAY_SPOTS if p not in self.state)

    def __iter__(self):
        return ((p, self.state.positions[p]) for p in HALLWAY_SPOTS if p in self.state)

    def blocked(self, start: int, stop: int) -> bool:
        xs = range(start + 1, stop + 1) if stop >= start else range(stop, start)
        return any(self._translate(x) in self.state for x in xs)


def steps_between(start: Position, stop: Position) -> int:
    match start, stop:
        case (x0, 0), (x1, 0):
            return abs(x0 - x1)
        case (x0, y0), (x1, y1) if x0 == x1:
            return abs(y1 - y0)
        case (x0, y0), (x1, y1):
            return (
                steps_between((x0, y0), (x0, 0))
                + steps_between((x0, 0), (x1, 0))
                + steps_between((x1, 0), (x1, y1))
            )
        case _:
            assert False, "Unhandled steps"


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


def read() -> Iterator[tuple[Position, Amphipod]]:
    with open("d23/input.txt") as f:
        for y, line in enumerate(islice(f, 1, None)):
            for x, c in enumerate(line[1:]):
                if c not in {"A", "B", "C", "D"}:
                    continue
                yield (x, y), cast(Amphipod, c)


def load(board: Iterator[tuple[Position, Amphipod]], room_size: int = 2) -> State:
    """
    >>> expected = State(
    ...     frozenset(
    ...         [
    ...             ((2, 1), "B"),
    ...             ((2, 2), "D"),
    ...             ((4, 1), "A"),
    ...             ((4, 2), "C"),
    ...             ((6, 1), "A"),
    ...             ((6, 2), "B"),
    ...             ((8, 1), "D"),
    ...             ((8, 2), "C"),
    ...         ]
    ...     )
    ... )
    >>> load(read()) == expected
    True
    """

    return State(frozenset(board), room_size=room_size)


if __name__ == "__main__":
    initial = load(read())
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
