from typing import Collection, Iterable, Iterator


def read() -> Iterator[int]:
    with open("d7/input.txt") as f:
        return (int(s) for s in f.read().strip().split(','))


def costs(starting: Iterable[int], position: int) -> Iterator[int]:
    for pos in starting:
        yield abs(position - pos)


def check_positions(starting: Collection[int]) -> Iterator[tuple[int, int]]:
    for position in range(min(starting), max(starting) + 1):
        yield position, sum(costs(starting, position))


if __name__ == "__main__":
    starting = list(read())
    print(min(check_positions(starting), key=lambda a: a[1]))
