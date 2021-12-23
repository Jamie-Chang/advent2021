from dataclasses import dataclass, field
from itertools import product
from typing import Iterable, Iterator, TypeAlias, cast, overload

import parse

Coord: TypeAlias = tuple[int, int, int]
Range: TypeAlias = tuple[int, int]
CubeOp: TypeAlias = tuple[bool, Range, Range, Range]
CubeOps: TypeAlias = Iterator[CubeOp]

FORMAT = parse.compile("{state:l} x={x0:d}..{x1:d},y={y0:d}..{y1:d},z={z0:d}..{z1:d}")


def read() -> Iterator[str]:
    with open("d22/input.txt") as f:
        for line in f:
            yield line.strip()


@dataclass
class Reactor:
    """
    >>> reactor = Reactor()
    >>> reactor[-1:2, -1:2, -1:2] = True
    >>> reactor[-1, -1, -1]
    True
    >>> reactor.count()
    27
    """

    cubes_on: set[Coord] = field(default_factory=set)

    @overload
    def __setitem__(self, key: Coord, value: bool) -> None:
        ...

    @overload
    def __setitem__(self, key: tuple[slice, slice, slice], value: bool) -> None:
        ...

    def __setitem__(self, key, value: bool) -> None:
        if all(isinstance(v, slice) for v in key):
            for cube in product(*(range(s.start, s.stop) for s in key)):
                self[cast(Coord, cube)] = value
            return

        if value:
            self.cubes_on.add(key)
        else:
            self.cubes_on.discard(key)

    def __getitem__(self, key: Coord) -> bool:
        return key in self.cubes_on

    def count(self):
        return len(self.cubes_on)


def bound(cubes: CubeOps, bounds: tuple[int, int] = (-50, 51)) -> CubeOps:
    """Filter cubes out of `bounds`."""
    for cube in cubes:
        _, *dimentions = cube
        if any(lo < bounds[0] or hi > bounds[1] for lo, hi in dimentions):
            continue
        yield cube


def load(lines: Iterable[str]) -> CubeOps:
    for line in lines:
        result = cast(parse.Result | None, FORMAT.parse(line))
        assert result is not None
        yield (
            result["state"] == "on",
            (result["x0"], result["x1"] + 1),
            (result["y0"], result["y1"] + 1),
            (result["z0"], result["z1"] + 1),
        )


if __name__ == "__main__":
    reactor = Reactor()
    for state, (x0, x1), (y0, y1), (z0, z1) in bound(load(read())):
        reactor[
            x0:x1,
            y0:y1,
            z0:z1,
        ] = state
    print(reactor.count())
