from typing import Iterable, Iterator


def read() -> Iterator[int]:
    with open("d6/input.txt") as f:
        return (int(s) for s in f.read().strip().split(','))


def day(ages: Iterable[int]) -> Iterator[int]:
    """
    >>> ages = [1, 2, 3, 4, 5, 6, 0]
    >>> list(day(ages))
    [0, 1, 2, 3, 4, 5, 6, 8]
    """
    new_fishes = 0
    for age in ages:
        if age == 0:
            new_fishes += 1
            yield 6

        else:
            yield age - 1

    for _ in range(new_fishes):
        yield 8


def ilen(iterable: Iterable) -> int:
    return sum(1 for _ in iterable)


if __name__ == "__main__":
    ages = read()
    for _ in range(80):
        ages = day(ages)

    print(ilen(ages))
