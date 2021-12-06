from dataclasses import dataclass
from typing import Hashable, Iterable, Iterator, TypeVar, cast

import parse

line_format = parse.compile("{x1:d},{y1:d} -> {x2:d},{y2:d}")


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


def read() -> Iterator[str]:
    with open("d5/input.txt") as f:
        for line in f:
            yield line.strip()


def parse_coords(lines: Iterable[str]) -> Iterator[tuple[Coord, Coord]]:
    """
    >>> lines = ["795,887 -> 541,887"]
    >>> list(parse_coords(lines))
    [(Coord(x=795, y=887), Coord(x=541, y=887))]
    """
    for line in lines:
        result = cast(parse.Result, line_format.parse(line))
        yield Coord(result["x1"], result["y1"]), Coord(result["x2"], result["y2"])


def generate_points(start: Coord, finish: Coord) -> Iterator[Coord]:
    match start, finish:
        case Coord(x=x1, y=s), Coord(x=x2, y=f) if x1 == x2:
            ys = range(s, f + 1) if f >= s else range(f, s + 1)
            for y in ys:
                yield Coord(x1, y)
        case Coord(x=s, y=y1), Coord(x=f, y=y2) if y1 == y2:
            xs = range(s, f + 1) if f >= s else range(f, s + 1)
            for x in xs:
                yield Coord(x, y1)


def get_coords(lines: Iterable[tuple[Coord, Coord]]) -> Iterator[Coord]:
    for line in lines:
        yield from generate_points(*line)


T = TypeVar("T", bound=Hashable)


def duplicates(it: Iterable[T]) -> Iterator[T]:
    existing = set()
    for element in it:
        if element in existing:
            yield element

        existing.add(element)


if __name__ == "__main__":
    coords = get_coords(parse_coords(read()))
    print(len(set(duplicates(coords))))
