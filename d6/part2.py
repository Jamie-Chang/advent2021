from collections import Counter
from typing import Iterable, TypeAlias

from part1 import read

Age: TypeAlias = int


def get_count(ages: Iterable[int]) -> Counter[Age]:
    """
    >>> get_count([1, 1, 8])
    Counter({1: 2, 8: 1})
    """
    count = Counter()
    for a in ages:
        count[a] += 1
    return count


def _day(count: Counter[Age]) -> Iterable[tuple[Age, int]]:
    for age, num in count.items():
        if age in (0, 7):
            continue

        yield age - 1, num

    yield 6, count[7] + count[0]
    yield 8, count[0]



def day(count: Counter[Age]) -> Counter[Age]:
    """
    >>> day(Counter({0: 8, 8: 1})) == {6: 8, 8: 8, 7: 1}
    True
    """
    return Counter(dict(_day(count)))


def total(count: Counter[Age]) -> int:
    return sum(count.values())


if __name__ == "__main__":
    ages = get_count(read())
    for _ in range(256):
        ages = day(ages)

    print(total(ages))
