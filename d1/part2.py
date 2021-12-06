from typing import Iterator
from itertools import islice, tee


def read() -> Iterator[int]:
    with open("d1/input.txt") as f:
        for line in f:
            yield int(line.strip())


def triplets(singles: Iterator[int]) -> Iterator[tuple[int, int, int]]:
    iterators = tee(singles, 3)
    return zip(
        iterators[0],
        islice(iterators[1], 1, None),
        islice(iterators[2], 2, None)
    )


def windowed(distances: Iterator[int]) -> Iterator[int]:
    for values in triplets(distances):
        yield sum(values)


def get_increases(distances: Iterator[int]):
    total = 0

    prev = None
    for distance in distances:
        if prev is not None and distance > prev:
            total += 1

        prev =  distance
    return total


if __name__ == "__main__":
    print(get_increases(windowed(read())))
