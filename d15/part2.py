import itertools
import math
from dataclasses import dataclass
from typing import Generic, Iterator, TypeAlias, TypeVar

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

    @classmethod
    def empty(cls, width: int, height: int, default: T) -> "Grid":
        return cls([[default for _ in range(width)] for _ in range(height)])

    def __getitem__(self, position: Position) -> T:
        return self.grid[position[0]][position[1]]

    def __setitem__(self, position: Position, value: T) -> None:
        self.grid[position[0]][position[1]] = value

    def successors(self, position: Position) -> Iterator[Position]:
        row, col = position
        if row + 1 < self.height:
            yield row + 1, col
        if col + 1 < self.width:
            yield row, col + 1

    def predecessors(self, position: Position) -> Iterator[Position]:
        row, col = position
        if row > 0:
            yield row - 1, col
        if col > 0:
            yield row, col - 1


def read() -> list[list[int]]:
    with open("d15/input.txt") as f:
        return [[int(c) for c in l.strip()] for l in f]


def expand_map(grid: Grid[int]) -> Grid[int]:
    """
    >>> grid = Grid([[8]])
    >>> expected = Grid(
    ...     [
    ...         [8, 9, 1, 2, 3],
    ...         [9, 1, 2, 3, 4],
    ...         [1, 2, 3, 4, 5],
    ...         [2, 3, 4, 5, 6],
    ...         [3, 4, 5, 6, 7],
    ...     ]
    ... )
    >>> expand_map(grid) == expected
    True
    """
    expanded = grid.empty(grid.width * 5, grid.height * 5, 0)

    for addition in itertools.product(range(5), range(5)):
        for p in itertools.product(range(grid.height), range(grid.width)):
            position = (
                p[0] + addition[0] * grid.height,
                p[1] + addition[1] * grid.width,
            )
            value = (grid[p] + sum(addition)) % 9
            expanded[position] = value if value > 0 else 9

    return expanded


def forward_scores(
    risks: Grid[int],
    scores: Grid[float],
    changed: set[Position],
) -> set[Position]:
    """Consider scores moving forwards (Down or Right)."""

    new = set()
    for c in itertools.product(range(risks.height), range(risks.width)):
        for predecessor in risks.predecessors(c):
            if predecessor not in changed and predecessor not in new:
                continue
            score = scores[predecessor] + risks[c]

            if score < scores[c]:
                scores[c] = score
                new.add(c)

    return new


def backward_scores(
    risks: Grid[int],
    scores: Grid[float],
    changed: set[Position],
) -> set[Position]:
    """Consider scores moving backwards (Up or Left)."""

    new = set()
    reverse = itertools.product(
        range(risks.height - 1, -1, -1),
        range(risks.width - 1, -1, -1),
    )
    for c in reverse:
        for successor in risks.successors(c):
            if successor not in changed and successor not in new:
                continue

            score = scores[successor] + risks[c]
            if score < scores[c]:
                scores[c] = score
                new.add(c)

    return new


def generate_scores(risks):
    scores: Grid[float] = Grid.empty(risks.width, risks.height, math.inf)
    scores[0, 0] = 0
    changes = {(0, 0)}
    for attempt in itertools.count(1):
        print(f"Attempt {attempt}, {len(changes) = }")
        if not changes:
            break
        changes = forward_scores(risks, scores, changes)
        changes = backward_scores(risks, scores, changes)

    return scores


if __name__ == "__main__":
    risks = expand_map(Grid(read()))
    scores = generate_scores(risks)
    print(scores[risks.height - 1, risks.width - 1])
