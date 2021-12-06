from typing import Iterable, Iterator, TypeAlias

Age: TypeAlias = int


def read() -> Iterator[int]:
    with open("d6/input.txt") as f:
        return (int(s) for s in f.read().strip().split(","))


def get_count(ages: Iterable[int]) -> dict[Age, int]:
    """
    >>> get_count([1, 1, 8])
    {1: 2, 8: 1}
    """
    count = {}
    for a in ages:
        if a not in count:
            count[a] = 0
        count[a] += 1
    return count


def _day(count: dict[Age, int]) -> Iterable[tuple[Age, int]]:
    for age, num in count.items():
        if age in (0, 7):
            continue

        yield age - 1, num

    new = count.get(0, 0)
    yield 6, count.get(7, 0) + new
    yield 8, new


def _filter_empty(counts: Iterable[tuple[Age, int]]) -> Iterable[tuple[Age, int]]:
    for i, c in counts:
        if c == 0:
            continue
        yield i, c


def day(count: dict[Age, int]) -> dict[Age, int]:
    """
    >>> day({0: 8, 8: 1}) == {6: 8, 8: 8, 7: 1}
    True
    """
    return dict(_filter_empty(_day(count)))


def total(count: dict[Age, int]) -> int:
    return sum(count.values())


if __name__ == "__main__":
    ages = get_count(read())
    for _ in range(256):
        ages = day(ages)

    print(total(ages))
