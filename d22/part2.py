from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Iterator, ParamSpec, TypeAlias

from part1 import CubeOps, load, read

Range: TypeAlias = tuple[int, int]

P = ParamSpec("P")


def filter_empty(fn: Callable[P, Iterator[Cube]]) -> Callable[P, Iterator[Cube]]:
    """Decorator to filter empty cubes from returned iterator"""

    def _new_fn(*args, **kwargs):
        for cube in fn(*args, **kwargs):
            if not cube:
                continue
            yield cube

    return _new_fn


@dataclass(frozen=True)
class Cube:
    x: Range
    y: Range
    z: Range

    def __bool__(self) -> bool:
        return self.volume() > 0

    def volume(self) -> int:
        """
        >>> Cube((0, 1), (-2, 0), (-1, 2)).volume()
        6
        >>> Cube((0, -10), (-2, 0), (-1, 2)).volume()
        0
        >>> Cube(x=(10, 10), y=(10, 10), z=(10, 10)).volume()
        0
        """
        return (
            max(0, self.x[1] - self.x[0])
            * max(0, self.y[1] - self.y[0])
            * max(0, self.z[1] - self.z[0])
        )

    def __getitem__(self, position: tuple[slice, slice, slice]) -> Cube:
        """
        >>> cube = Cube((0, 10), (0, 10), (0, 10))
        >>> cube[5:, :, :]
        Cube(x=(5, 10), y=(0, 10), z=(0, 10))
        >>> cube[5:, 5:, 5:]
        Cube(x=(5, 10), y=(5, 10), z=(5, 10))
        >>> bool(cube[10:, :, :])
        False
        >>> cube[:5, :5, :5]
        Cube(x=(0, 5), y=(0, 5), z=(0, 5))
        >>> cube[2:5, 2:5, 2:5]
        Cube(x=(2, 5), y=(2, 5), z=(2, 5))
        """
        x, y, z = position
        assert x.step is None
        assert y.step is None
        assert z.step is None
        return Cube(
            x=_merge_slice(self.x, x),
            y=_merge_slice(self.y, y),
            z=_merge_slice(self.z, z),
        )

    @filter_empty
    def __sub__(self, other: Cube) -> Iterator[Cube]:
        """
        >>> cubes = Cube((0, 10), (0, 10), (0, 10)) - Cube((4, 6), (4, 6), (4, 6))
        >>> total(cubes)
        992

        >>> cubes = Cube((0, 10), (0, 10), (0, 10)) - Cube((5, 10), (5, 10), (5, 10))
        >>> cubes = list(cubes)
        >>> len(cubes)
        3

        >>> cubes = Cube((0, 10), (0, 10), (0, 10)) - Cube((-1, 0), (-1, 0), (-1, 0))
        >>> len(cubes)
        1
        """
        if not self & other:
            yield self
            return

        yield self[: other.x[0], :, :]
        yield self[other.x[1] :, :, :]
        yield self[other.x[0] : other.x[1], : other.y[0], :]
        yield self[other.x[0] : other.x[1], other.y[1] :, :]
        yield self[other.x[0] : other.x[1], other.y[0] : other.y[1], : other.z[0]]
        yield self[other.x[0] : other.x[1], other.y[0] : other.y[1], other.z[1] :]

    def __and__(self, other: Cube) -> Cube:
        """
        >>> Cube(x=(11, 14), y=(11, 14), z=(11, 14)) & Cube(x=(10, 13), y=(10, 13), z=(10, 13))
        Cube(x=(11, 13), y=(11, 13), z=(11, 13))
        """
        return Cube(
            (max(self.x[0], other.x[0]), min(self.x[1], other.x[1])),
            (max(self.y[0], other.y[0]), min(self.y[1], other.y[1])),
            (max(self.z[0], other.z[0]), min(self.z[1], other.z[1])),
        )


def _merge_slice(r: Range, s: slice):
    start, stop = r
    if s.start is not None:
        start = max(s.start, start)

    if s.stop is not None:
        stop = min(s.stop, stop)

    return start, stop


def on(cubes: Iterable[Cube], cube: Cube) -> Iterator[Cube]:
    """
    >>> cubes = [Cube(x=(10, 13), y=(10, 13), z=(10, 13))]
    >>> cube = Cube(x=(11, 14), y=(11, 14), z=(11, 14))
    >>> expected = [
    ...     Cube(x=(10, 11), y=(10, 13), z=(10, 13)),
    ...     Cube(x=(11, 13), y=(10, 11), z=(10, 13)),
    ...     Cube(x=(11, 13), y=(11, 13), z=(10, 11)),
    ...     Cube(x=(11, 14), y=(11, 14), z=(11, 14)),
    ... ]
    >>> result = list(on(cubes, cube))
    >>> assert result == expected, f"({result = }) != ({expected = })"
    """
    for c in cubes:
        intersection = c & cube
        if not intersection:
            yield c
            continue

        yield from c - intersection

    yield cube


def off(cubes: Iterable[Cube], cube: Cube) -> Iterator[Cube]:
    """
    >>> cubes = [Cube(x=(10, 13), y=(10, 13), z=(10, 13))]
    >>> cube = Cube(x=(11, 14), y=(11, 14), z=(11, 14))
    >>> expected = [
    ...     Cube(x=(10, 11), y=(10, 13), z=(10, 13)),
    ...     Cube(x=(11, 13), y=(10, 11), z=(10, 13)),
    ...     Cube(x=(11, 13), y=(11, 13), z=(10, 11)),
    ... ]
    >>> result = list(off(cubes, cube))
    >>> assert result == expected, f"({result = }) != ({expected = })"
    """
    for c in cubes:
        yield from c - cube


def reactor_reboot(operations: Iterator[tuple[Cube, bool]]) -> Iterator[Cube]:
    cubes = iter([])
    for cube, state in operations:
        cubes = on(cubes, cube) if state else off(cubes, cube)
    return cubes


def load_cubes(data: CubeOps) -> Iterator[tuple[Cube, bool]]:
    for state, *dimentions in data:
        yield Cube(*dimentions), state


def total(cubes: Iterable[Cube]) -> int:
    return sum(c.volume() for c in cubes)


if __name__ == "__main__":
    cubes = reactor_reboot(load_cubes(load(read())))
    print(total(cubes))
