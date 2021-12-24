from collections import UserDict
from itertools import product
from typing import Iterable, Literal, TypeVar

from alu import ALU, load, read


def propagate(key: int, value: int):
    """Change the values of related keys."""
    yield key, value
    while True:
        match key:
            case 0:
                key, value = 13, value + 6
            case 1:
                key, value = 12, value - 2
            case 2:
                key, value = 11, value + 5
            case 3:
                key, value = 4, value - 5
            case 5:
                key, value = 10, value + 8
            case 6:
                key, value = 7, value - 4
            case 8:
                key, value = 9, value + 2
            case _:
                break

        yield key, value


class DigitDict(UserDict[int, int]):
    def __setitem__(self, key: int, item: int) -> None:
        if not 0 < item <= 9:
            raise ValueError(item)
        return super().__setitem__(key, item)


def values(direction: Literal[-1, 1] = 1):
    numbers = product(
        ((0, v) for v in range(1, 10)[::direction]),
        ((1, v) for v in range(1, 10)[::direction]),
        ((2, v) for v in range(1, 10)[::direction]),
        ((3, v) for v in range(1, 10)[::direction]),
        ((5, v) for v in range(1, 10)[::direction]),
        ((6, v) for v in range(1, 10)[::direction]),
        ((8, v) for v in range(1, 10)[::direction]),
    )
    for values in numbers:
        mapping = DigitDict(dict(values))
        try:
            for k, v in values:
                mapping.update(propagate(k, v))
        except ValueError:
            continue

        yield int("".join(str(mapping[i]) for i in range(14)))


T = TypeVar("T")


def first(it: Iterable[T]) -> T:
    for v in it:
        return v
    assert False


if __name__ == "__main__":
    result = first(values(-1))
    alu_result = ALU().execute(load(read()), result)
    assert alu_result == 0, f"ALU return non-zero ({alu_result}) for ({result = })"
    print(result)
