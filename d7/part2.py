from typing import Collection, Iterator


def read() -> Iterator[int]:
    with open("d7/input.txt") as f:
        return (int(s) for s in f.read().strip().split(','))


def fuel_cost(starting: int, end: int) -> int:
    """
    >>> fuel_cost(5, 2)
    6
    """
    distance = abs(starting - end)
    cost =  distance * (distance + 1) / 2
    assert cost == int(cost), "cost must always be exact"
    return int(cost)


def check_costs(positions: Collection[int]) -> Iterator[tuple[int, int]]:
    for position in range(min(positions), max(positions) + 1):
        yield position, sum(fuel_cost(p, position) for p in positions)


if __name__ == "__main__":
    print(min(check_costs(list(read())), key=lambda a: a[1]))
