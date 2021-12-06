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


def parse_lines(lines: Iterable[str]) -> Iterator[tuple[Coord, Coord]]:
    """
    >>> lines = ["795,887 -> 541,887"]
    >>> list(parse_lines(lines))
    [(Coord(x=795, y=887), Coord(x=541, y=887))]
    """
    for line in lines:
        result = cast(parse.Result, line_format.parse(line))
        yield Coord(result["x1"], result["y1"]), Coord(result["x2"], result["y2"])


def _get_steps(start: int, finish: int) -> Iterable[int]:
    if start > finish:
        return range(start, finish -1, -1)
    return range(start, finish + 1)


def trace_line(start: Coord, finish: Coord) -> Iterator[Coord]:
    """
    >>> list(trace_line(Coord(0, 8), Coord(1, 7)))
    [Coord(x=0, y=8), Coord(x=1, y=7)]
    >>> list(trace_line(Coord(6, 4), Coord(5, 3)))
    [Coord(x=6, y=4), Coord(x=5, y=3)]
    >>> list(trace_line(Coord(6, 4), Coord(0, 0)))
    []
    """
    match start, finish:
        case Coord(x=x1, y=y1), Coord(x=x2, y=y2) if x1 == x2:
            for y in _get_steps(y1, y2):
                yield Coord(x1, y)

        case Coord(x=x1, y=y1), Coord(x=x2, y=y2) if y1 == y2:
            for x in _get_steps(x1, x2):
                yield Coord(x, y1)

        case Coord(x=x1, y=y1), Coord(x=x2, y=y2) if abs(x1 - x2) == abs(y1 - y2):
            for x, y in zip(_get_steps(x1, x2), _get_steps(y1, y2)):
                yield Coord(x, y)


def get_coords(lines: Iterable[tuple[Coord, Coord]]) -> Iterator[Coord]:
    for line in lines:
        yield from trace_line(*line)


T = TypeVar("T", bound=Hashable)


def duplicates(it: Iterable[T]) -> Iterator[T]:
    existing = set()
    for element in it:
        if element in existing:
            yield element

        existing.add(element)


if __name__ == "__main__":
    coords = get_coords(parse_lines(read()))
    print(len(set(duplicates(coords))))
