from typing import Iterator


def read() -> Iterator[int]:
    with open("d1/input.txt") as f:
        for line in f:
            yield int(line.strip())


def get_increases(distances: Iterator[int]):
    total = 0

    prev = None
    for distance in distances:
        if prev is not None and distance > prev:
            total += 1

        prev =  distance
    return total


if __name__ == "__main__":
    print(get_increases(read()))
