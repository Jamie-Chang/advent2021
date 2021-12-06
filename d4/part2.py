from dataclasses import dataclass, field
from typing import Iterator, TypeVar

Pos = tuple[int, int]


def parse_line(line: str) -> Iterator[int]:
    for i in range(0, len(line), 3):
        yield int(line[i : i + 3].strip())


def parse_board_items(string: str) -> Iterator[tuple[Pos, int]]:
    for row, line in enumerate(string.splitlines()):
        for col, value in enumerate(parse_line(line)):
            yield (row, col), value


@dataclass
class Board:
    height: int
    width: int
    values: dict[int, set[Pos]]
    marked: set[Pos] = field(init=False, default_factory=set)

    def __hash__(self) -> int:
        return id(self)

    def items(self):
        for value, positions in self.values.items():
            for position in positions:
                yield position, value

    @property
    def total_unmarked(self):
        return sum(v for p, v in self.items() if p not in self.marked)

    @classmethod
    def from_str(cls, string: str) -> "Board":
        values = {}
        last_position = None
        for position, value in parse_board_items(string):
            values.setdefault(value, set()).add(position)
            last_position = position

        assert last_position is not None
        return cls(
            height=last_position[0] + 1,
            width=last_position[1] + 1,
            values=values,
        )

    def check_row(self, row: int) -> bool:
        return all((row, col) in self.marked for col in range(self.width))

    def check_col(self, col: int) -> bool:
        return all((row, col) in self.marked for row in range(self.height))

    def check(self, row: int, col: int) -> dict:
        if self.check_row(row):
            return {"row": row}

        if self.check_col(col):
            return {"col": col}

        return {}

    def mark(self, value: int) -> Iterator[Pos]:
        if value not in self.values:
            return

        for pos in self.values[value]:
            self.marked.add(pos)
            yield pos


def read() -> tuple[list[int], set[Board]]:
    with open("d4/input.txt") as f:
        data = f.read().split("\n\n")
        calls = [int(i) for i in data[0].split(",")]
        boards = {Board.from_str(string) for string in data[1:]}
        return calls, boards


def play(calls: list[int], boards: set[Board]) -> Iterator[tuple[int, Board]]:
    for call in calls:
        remaining = set()
        for board in boards:
            for pos in board.mark(call):
                if board.check(*pos):
                    yield call, board
                    break
            else:
                remaining.add(board)

        boards = remaining


T = TypeVar("T")


def last(iter: Iterator[T]) -> T:
    last = None
    for i in iter:
        last = i

    if last is None:
        raise ValueError("Empty iterator")
    return last


if __name__ == "__main__":
    call, board = last(play(*read()))
    print(call * board.total_unmarked)
