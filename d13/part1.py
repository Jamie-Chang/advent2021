from typing import Iterable, Iterator, Literal, TypeAlias, cast

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


if __name__ == "__main__":
    lines = read()
    coords = list(parse_coords(lines))
    folds = list(parse_folds(lines))

    print(len(set(do_fold(coords, folds[0]))))
