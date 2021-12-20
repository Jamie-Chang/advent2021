from __future__ import annotations
from functools import cached_property

import itertools
from dataclasses import dataclass, field
from typing import Iterator, Literal, TypeAlias, cast

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
    ((-2, -2), (3, 4))
    >>> image[0, 1]
    1
    >>> len(list(image.keys()))
    30
    """

    pixel_type: PixelValue = 1
    pixels: set[Position] = field(default_factory=set)
    bounds: tuple[Position, Position] = (-2, -2), (3, 3)

    @property
    def other_type(self) -> PixelValue:
        return other(self.pixel_type)

    def __getitem__(self, position: Position) -> PixelValue:
        return self.pixel_type if position in self.pixels else self.other_type

    def __setitem__(self, position: Position, value: PixelValue) -> None:
        assert value in (0, 1)
        if value != self.pixel_type:
            self.pixels.discard(position)
            return

        self.pixels.add(position)
        self.bounds = (
            (
                min(self.bounds[0][0], position[0] - BORDER_WIDTH),
                min(self.bounds[0][1], position[1] - BORDER_WIDTH),
            ),
            (
                max(self.bounds[1][0], position[0] + BORDER_WIDTH + 1),
                max(self.bounds[1][1], position[1] + BORDER_WIDTH + 1),
            ),
        )

    def __iter__(self):
        return self.keys()

    def keys(self) -> Iterator[Position]:
        start, end = self.bounds
        return itertools.product(range(start[0], end[0]), range(start[1], end[1]))

    def values(self) -> Iterator[PixelValue]:
        for k in self.keys():
            yield self[k]

    def items(self) -> Iterator[tuple[Position, PixelValue]]:
        for k in self.keys():
            yield k, self[k]

    def display(self) -> None:
        start, end = self.bounds
        for y in range(start[1], end[1]):
            print("".join("#" if self[x, y] else " " for x in range(start[0], end[0])))

    @property
    def count(self) -> int:
        return len(self.pixels)


def get_next_value(
    algorithm: Algorithm,
    image: Image,
    position: Position,
) -> PixelValue:
    positions = (
        (x, y)
        for y, x in itertools.product(
            range(position[1] - 1, position[1] + 2),
            range(position[0] - 1, position[0] + 2),
        )
    )
    return algorithm[int("".join(str(image[p]) for p in positions), base=2)]


def other(value: PixelValue) -> PixelValue:
    return 0 if value == 1 else 1


def next_image(algorithm: Algorithm, image: Image) -> Image:
    next_image = Image(other(algorithm[int(str(image.other_type) * 9, base=2)]))

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
    image = Image(1)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            image[x, y] = 1 if c == "#" else 0

    return image


def load(lines: Iterator[str]) -> tuple[Algorithm, Image]:
    return read_algorithm(lines), read_image(lines)


if __name__ == "__main__":
    algorithm, image = load(read())
    for _ in range(2):
        image = next_image(algorithm, image)
    print(image.count)
