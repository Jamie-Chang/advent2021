"""NOTE: This solution is in complete as it'll only move Down and Right.

This happens to work, for full solution see part2.
"""

from dataclasses import dataclass
from typing import Generic, Iterator, TypeAlias, TypeVar, cast

Position: TypeAlias = tuple[int, int]

T = TypeVar("T")


@dataclass
class Grid(Generic[T]):
    grid: list[list[T]]

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    def __getitem__(self, position: Position) -> T:
        return self.grid[position[0]][position[1]]

    def __setitem__(self, position: Position, value: T) -> None:
        self.grid[position[0]][position[1]] = value


def read() -> list[list[int]]:
    with open("d15/input.txt") as f:
        return [[int(c) for c in l.strip()] for l in f]


def predecessors(position: Position) -> Iterator[Position]:
    row, col = position
    if row > 0:
        yield row - 1, col
    if col > 0:
        yield row, col - 1


def generate_scores(risks: Grid[int]) -> Grid[int]:

    scores: Grid[int | None] = Grid([[None] * risks.width] * risks.height)

    for r in range(risks.height):
        for c in range(risks.width):
            risk = risks[r, c]
            scores[r, c] = min(
                (cast(int, scores[p]) + risk for p in predecessors((r, c))),
                default=0,
            )

    return cast(Grid[int], scores)


if __name__ == "__main__":
    risks = Grid(read())
    print(generate_scores(risks)[risks.height - 1, risks.width - 1])
