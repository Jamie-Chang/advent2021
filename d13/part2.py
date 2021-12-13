from typing import Collection, Iterable, Iterator, Literal, TypeAlias, cast

import parse

COORD_FORMAT = parse.compile("{:d},{:d}")
FOLD_FORMAT = parse.compile("fold along {axis:l}={value:d}")
Fold: TypeAlias = tuple[Literal["x", "y"], int]
Coord: TypeAlias = tuple[int, int]


def read() -> Iterator[str]:
    with open("d13/input.txt") as f:
        for line in f:
            yield line.strip()


def parse_coords(lines: Iterable[str]) -> Iterator[Coord]:
    for line in lines:
        if not line:
            return

        result = cast(parse.Result, COORD_FORMAT.parse(line))
        yield result[0], result[1]


def parse_folds(lines: Iterable[str]) -> Iterator[Fold]:
    for line in lines:
        result = cast(parse.Result, FOLD_FORMAT.parse(line))
        yield result['axis'], result['value']


def do_fold(coords: Iterable[Coord], fold: Fold) -> Iterator[Coord]:
    for coord in coords:
        match coord, fold:
            case (x, y), ("x", x_fold) if x > x_fold:
                yield 2 * x_fold - x, y

            case (x, y), ("y", y_fold) if y > y_fold:
                yield x, 2 * y_fold - y

            case _:
                yield coord


def dimentions(coords: Collection) -> tuple[int, int]:
    return max(x for x, _ in coords) + 1, max(y for y, _ in coords) + 1


def display(coords: set[Coord]) -> None:
    width, height = dimentions(coords)
    for y in range(height):
        for x in range(width):
            print("#" if (x, y) in coords else " ", end="")
        print()


if __name__ == "__main__":
    lines = read()
    coords = list(parse_coords(lines))
    for fold in parse_folds(lines):
        coords = do_fold(coords, fold)

    display(set(coords))
