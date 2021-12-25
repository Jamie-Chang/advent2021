from __future__ import annotations

from dataclasses import dataclass
from itertools import chain
from typing import Iterable, Iterator


def read() -> Iterator[str]:
    with open("d25/input.txt") as f:
        for l in f:
            yield l.strip()


def parse_row(line: str):
    east = Vector(x=1, y=0)
    south = Vector(x=0, y=1)
    for character in line:
        match character:
            case ".":
                yield None

            case "v":
                yield SeaCucumber(south)

            case ">":
                yield SeaCucumber(east)


def load(lines: Iterable[str]):
    return Board([list(parse_row(line)) for line in lines])


@dataclass(frozen=True, eq=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        """
        >>> Vector(1, 2) + Vector(2, 1)
        Vector(x=3, y=3)
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector) -> Vector:
        """
        >>> Vector(1, 2) - Vector(2, 1)
        Vector(x=-1, y=1)
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __iter__(self) -> Iterator[int]:
        yield self.x
        yield self.y

    def __mod__(self, other: Vector) -> Vector:
        """
        >>> Vector(-1, -1) % Vector(5, 5)
        Vector(x=4, y=4)
        >>> Vector(6, 6) % Vector(5, 5)
        Vector(x=1, y=1)
        """
        return Vector(self.x % other.x, self.y % other.y)

    def __getitem__(self, p: int) -> int:
        if p == 0:
            return self.x
        if p == 1:
            return self.y

        raise IndexError(p)


@dataclass
class SeaCucumber:
    direction: Vector


@dataclass
class Board:
    board: list[list[SeaCucumber | None]]

    def __setitem__(self, key: Vector, value: SeaCucumber | None):
        self.board[key.y][key.x] = value

    def __getitem__(self, key: Vector) -> SeaCucumber | None:
        return self.board[key.y][key.x]

    def pop(self, key: Vector) -> SeaCucumber | None:
        value = self[key]
        self[key] = None
        return value

    def __iter__(self) -> Iterator[Vector]:
        width, height = self.size
        for y in range(height):
            for x in range(width):
                yield Vector(x, y)

    @property
    def size(self) -> Vector:
        if not self.board:
            return Vector(0, 0)

        return Vector(len(self.board[0]), len(self.board))


def movements(board: Board, direction: Vector) -> dict[Vector, Vector]:
    return dict(_movements(board, direction))


def _movements(board: Board, direction: Vector) -> Iterator[tuple[Vector, Vector]]:
    for start in board:
        value = board[start]
        if value is None:
            continue

        if value.direction != direction:
            continue

        stop = (start + value.direction) % board.size
        if board[stop] is None:
            yield start, stop


def step(board: Board):
    east = Vector(1, 0)
    south = Vector(0, 1)
    changed = False

    for start, stop in movements(board, east).items():
        changed = True
        board[stop] = board.pop(start)

    for start, stop in movements(board, south).items():
        changed = True
        board[stop] = board.pop(start)

    return changed


def move(board: Board) -> Iterator[Board]:
    while step(board):
        yield board


def ilen(it: Iterable) -> int:
    return sum(1 for _ in it)


def display(value: SeaCucumber | Board | None) -> str:
    match value:
        case SeaCucumber(Vector(0, 1)):
            return "v"

        case SeaCucumber(Vector(1, 0)):
            return ">"

        case None:
            return "."

        case Board() as b:
            return "\n".join("".join(display(item) for item in row) for row in b.board)

        case _:
            assert False, value


if __name__ == "__main__":
    print(ilen(move(load(read()))) + 1)
