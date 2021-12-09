from typing import Iterator


def read() -> list[list[int]]:
    with open("d9/input.txt") as f:
        return [[int(c) for c in l.strip()] for l in f]


def _adjacent_coord(row: int, col: int) -> Iterator[tuple[int, int]]:
    yield row - 1, col
    yield row + 1, col
    yield row, col - 1
    yield row, col + 1


def _in_bound(rows: int, cols: int, row: int, col: int) -> bool:
    return 0 <= row < rows and 0 <= col < cols


def adjacent(grid: list[list[int]], row: int, col: int) -> Iterator[int]:
    rows = len(grid)
    cols = len(grid[0])
    for row, col in _adjacent_coord(row, col):
        if _in_bound(rows, cols, row, col):
            yield grid[row][col]


def get_low_points(grid: list[list[int]]) -> Iterator[int]:
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if all(value < v for v in adjacent(grid, r, c)):
                yield value


if __name__ == "__main__":
    grid = read()
    print(sum(height + 1 for height in get_low_points(grid)))
