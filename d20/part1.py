from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Iterator, Literal, TypeAlias

Position: TypeAlias = tuple[int, int]
PixelValue: TypeAlias = Literal[0, 1]
Algorithm: TypeAlias = list[PixelValue]

BORDER_WIDTH = 1


@dataclass
class Image:
    """
    >>> image = Image()
    >>> image[0, 1] = 1
    >>> image.bounds
    ((-1, 0), (2, 3))
    >>> image[0, 1]
    1
    >>> len(list(image.keys()))
    9
    """

    default: PixelValue = 0
    pixels: set[Position] = field(default_factory=set)
    bounds: tuple[Position, Position] | None = None

    def __getitem__(self, position: Position) -> PixelValue:
        return other(self.default) if position in self.pixels else self.default

    def __setitem__(self, position: Position, value: PixelValue) -> None:
        if value != other(self.default):
            self.pixels.discard(position)
            return

        self.pixels.add(position)
        bounds = (
            (
                position[0] - BORDER_WIDTH,
                position[1] - BORDER_WIDTH,
            ),
            (
                position[0] + BORDER_WIDTH + 1,
                position[1] + BORDER_WIDTH + 1,
            ),
        )
        self.bounds = (
            (
                (
                    min(self.bounds[0][0], bounds[0][0]),
                    min(self.bounds[0][1], bounds[0][1]),
                ),
                (
                    max(self.bounds[1][0], bounds[1][0]),
                    max(self.bounds[1][1], bounds[1][1]),
                ),
            )
            if self.bounds
            else bounds
        )

    def __iter__(self):
        return self.keys()

    def keys(self) -> Iterator[Position]:
        if self.bounds is None:
            return

        yield from itertools.product(self.row_keys(), self.col_keys())

    def row_keys(self) -> Iterator[int]:
        if self.bounds is None:
            return
        yield from range(self.bounds[0][0], self.bounds[1][0])

    def col_keys(self) -> Iterator[int]:
        if self.bounds is None:
            return

        yield from range(self.bounds[0][1], self.bounds[1][1])

    def values(self) -> Iterator[PixelValue]:
        for k in self.keys():
            yield self[k]

    def items(self) -> Iterator[tuple[Position, PixelValue]]:
        for k in self.keys():
            yield k, self[k]

    @property
    def count(self) -> int:
        return len(self.pixels)


def get_next_value(
    algorithm: Algorithm,
    image: Image,
    position: Position,
) -> PixelValue:
    positions = itertools.product(
        range(position[0] - 1, position[0] + 2),
        range(position[1] - 1, position[1] + 2),
    )
    return algorithm[int("".join(str(image[p]) for p in positions), base=2)]


def other(value: PixelValue) -> PixelValue:
    return 0 if value == 1 else 1


def next_image(algorithm: Algorithm, image: Image) -> Image:
    next_default = algorithm[int(str(image.default) * 9, base=2)]
    next_image = Image(next_default)

    for key in image:
        next_image[key] = get_next_value(algorithm, image, key)
    return next_image


def read() -> Iterator[str]:
    with open("d20/input.txt") as f:
        for line in f:
            yield line.strip()


def read_algorithm(lines: Iterator[str]) -> Algorithm:
    line = next(lines)
    next(lines)

    return [1 if c == "#" else 0 for c in line]


def read_image(lines: Iterator[str]) -> Image:
    image = Image()
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            image[row, col] = 1 if c == "#" else 0

    return image


def load(lines: Iterator[str]) -> tuple[Algorithm, Image]:
    return read_algorithm(lines), read_image(lines)


if __name__ == "__main__":
    algorithm, image = load(read())
    for _ in range(2):
        image = next_image(algorithm, image)
    print(image.count)
