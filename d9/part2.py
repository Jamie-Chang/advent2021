from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Iterator, TypeAlias

Coord: TypeAlias = tuple[int, int]


def read() -> list[list[int]]:
    with open("d9/input.txt") as f:
        return [[int(c) for c in l.strip()] for l in f]


@dataclass
class Grid:
    grid: list[list[int]]

    def __getitem__(self, coord: Coord) -> int:
        return self.grid[coord[0]][coord[1]]

    @cached_property
    def height(self):
        return len(self.grid)

    @cached_property
    def width(self):
        return len(self.grid[0])

    def adjacent(self, coord: Coord) -> Iterator[tuple[Coord, int]]:
        for neighbour in _adjacent_coord(coord):
            if _in_bound(self.height, self.width, neighbour):
                yield (neighbour), self[neighbour]

    def values(self) -> Iterator[tuple[Coord, int]]:
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                yield (r, c), value

    def low_points(self) -> Iterator[tuple[Coord, int]]:
        for coord, value in self.values():
            if all(value < v for _, v in self.adjacent(coord)):
                yield coord, value

    def basin(self, start: Coord) -> Iterator[tuple[Coord, int]]:
        """Get basin flowing towards `start`."""
        queue = [(start, self[start])]
        visited = set()
        while queue:
            point, height = queue.pop(0)
            if point in visited:
                continue
            yield point, height
            visited.add(point)
            queue.extend((c, v) for c, v in self.adjacent(point) if height < v < 9)


def _adjacent_coord(coord: Coord) -> Iterator[Coord]:
    """
    >>> set(_adjacent_coord((1, 1))) == {(0, 1), (1, 0), (2, 1), (1, 2)}
    True
    """
    row, col = coord
    yield row - 1, col
    yield row + 1, col
    yield row, col - 1
    yield row, col + 1


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


def ilen(it: Iterable) -> int:
    return sum(1 for _ in it)


def get_basin_sizes(grid: Grid) -> Iterator[int]:
    for low_point, _ in grid.low_points():
        yield ilen(grid.basin(low_point))


def product(values: Iterable[int]) -> int:
    total = 1
    for value in values:
        total *= value

    return total


if __name__ == "__main__":
    grid = Grid(read())
    print(product(sorted(get_basin_sizes(grid))[-3:]))
