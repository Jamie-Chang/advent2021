from itertools import product
import string
from collections import UserDict, defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Literal, TypeAlias, TypeVar, cast

Variable: TypeAlias = Literal["w", "x", "y", "z"]
Operation: TypeAlias = (
    tuple[Literal["inp"], Variable]
    | tuple[str, Variable, int]
    | tuple[str, Variable, Variable]
)


digs = string.ascii_uppercase


def base26(x: int):
    if x == 0:
        return digs[0]

    digits = []

    while x:
        digits.append(digs[x % 26])
        x = x // 26

    digits.reverse()

    return "".join(digits)


def read() -> Iterator[str]:
    with open("d24/input.txt") as f:
        for line in f:
            yield line.strip()


def load(lines: Iterable[str]) -> Iterator[Operation]:
    for line in lines:
        operation = line[:3]
        values = line[4:].split(" ")

        match values:
            case [str() as a]:
                yield cast(Literal["inp"], operation), cast(Variable, a)
            case [str() as a, str() as b]:
                try:
                    yield operation, cast(Variable, a), int(b)
                except ValueError:
                    yield operation, cast(Variable, a), cast(Variable, b)
            case _:
                assert False, line


@dataclass
class ALU:
    """The ALU generates a base 26 number.

    With each input base 10 digit it does one of the following:
    - Push a new base 26 digit at the end.
    - Remove the last base 26 digit generated.

    Suppose the inputs are i[0], i[1], ..., i[13], to completely remove all
    digits generated, the following must apply:
    - i[0] = i[13] - 6
    - i[1] = i[12] + 2
    - i[2] = i[11] - 5
    - i[3] = i[4] + 5
    - i[5] = i[10] - 8
    - i[6] = i[7] + 4
    - i[8] = i[9] - 2
    """

    data: dict[Variable, int] = field(default_factory=lambda: defaultdict(lambda: 0))

    def instruction(self, operation: Operation, inputs: list[int] | None = None):
        match operation:
            case "inp", a:
                self.data[a] = int(input().strip()) if inputs is None else inputs.pop(0)

            case "add", a, int() as b:
                self.data[a] += b

            case "add", a, str() as b:
                self.data[a] += self.data[b]

            case "mul", a, int() as b:
                self.data[a] *= b

            case "mul", a, str() as b:
                self.data[a] *= self.data[b]

            case "div", a, int() as b:
                self.data[a] //= b

            case "div", a, str() as b:
                self.data[a] //= self.data[b]

            case "mod", a, int() as b:
                self.data[a] %= b

            case "mod", a, str() as b:
                self.data[a] %= self.data[b]

            case "eql", a, int() as b:
                self.data[a] = 1 if self.data[a] == b else 0

            case "eql", a, str() as b:
                self.data[a] = 1 if self.data[a] == self.data[b] else 0

    def execute(
        self,
        operations: Iterable[Operation],
        inputs: list[int] | None = None,
    ):
        for op in operations:
            self.instruction(op, inputs)

        return self.data["z"]


def convert(i: int) -> list[int]:
    """
    >>> convert(1234)
    [1, 2, 3, 4]
    """
    return [int(n) for n in str(i)]


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
    assert (
        ALU().execute(
            operations=load(read()),
            inputs=convert(result),
        )
        == 0
    ), f"{result = } does not pass check"
    print(result)
