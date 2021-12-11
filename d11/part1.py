from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Iterator, TypeAlias


Coord: TypeAlias = tuple[int, int]


def read() -> list[list[int]]:
    with open("d11/input.txt") as f:
        return [[int(c) for c in l.strip()] for l in f]


def _adjacent_coord(coord: Coord) -> Iterator[Coord]:
    """
    >>> set(_adjacent_coord((1, 1))) == {
    ...     (0, 0),
    ...     (0, 2),
    ...     (2, 0),
    ...     (2, 2),
    ...     (0, 1),
    ...     (1, 0),
    ...     (2, 1),
    ...     (1, 2)
    ... }
    True
    """
    row, col = coord
    yield row - 1, col
    yield row + 1, col
    yield row, col - 1
    yield row, col + 1
    yield row - 1, col - 1
    yield row - 1, col + 1
    yield row + 1, col - 1
    yield row + 1, col + 1


def _in_bound(height: int, width: int, coord: Coord) -> bool:
    """
    >>> _in_bound(5, 5, (1, 1))
    True
    >>> _in_bound(5, 5, (-1, 0))
    False
    >>> _in_bound(5, 5, (5, 0))
    False
    """
    row, col = coord
    return 0 <= row < height and 0 <= col < width


@dataclass
class Grid:
    grid: list[list[int]]

    def __getitem__(self, coord: Coord) -> int:
        return self.grid[coord[0]][coord[1]]

    def __setitem__(self, coord: Coord, value: int) -> None:
        self.grid[coord[0]][coord[1]] = value

    @cached_property
    def height(self):
        return len(self.grid)

    @cached_property
    def width(self):
        return len(self.grid[0])

    def adjacent(self, coord: Coord) -> Iterator[Coord]:
        for neighbour in _adjacent_coord(coord):
            if _in_bound(self.height, self.width, neighbour):
                yield neighbour

    def keys(self) -> Iterator[Coord]:
        for r in range(self.height):
            for c in range(self.width):
                yield r, c


def get_flashing(grid: Grid) -> Iterable[Coord]:
    for coord in grid.keys():
        if grid[coord] > 9:
            yield coord


def step(grid: Grid) -> set[Coord]:
    for coord in grid.keys():
        grid[coord] += 1

    flashed = set()
    changed = True

    while changed:
        changed = False
        for coord in get_flashing(grid):
            if coord in flashed:
                continue

            changed = True
            flashed.add(coord)

            for adjacent in grid.adjacent(coord):
                grid[adjacent] += 1

    for coord in flashed:
        grid[coord] = 0

    return flashed


if __name__ == "__main__":
    grid = Grid(read())
    print(sum(len(step(grid)) for _ in range(100)))
