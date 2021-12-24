import string
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Literal, TypeAlias, cast

Variable: TypeAlias = Literal["w", "x", "y", "z"]
Operation: TypeAlias = (
    tuple[Literal["inp"], Variable]
    | tuple[str, Variable, int]
    | tuple[str, Variable, Variable]
)


def base26(number: int) -> str:
    """Generate a base 26 representation of `number`

    Namely:
    - 0  -> A
    - 1  -> B
    - ...
    - 25 -> Z
    """
    if number == 0:
        return string.ascii_uppercase[0]

    digits = []

    while number:
        digits.append(string.ascii_uppercase[number % 26])
        number //= 26

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
        number: int | None = None,
    ):
        inputs = convert(number) if number is not None else number
        for operation in operations:
            self.instruction(
                operation,
                inputs,
            )

        return self.data["z"]


def convert(i: int) -> list[int]:
    """
    >>> convert(1234)
    [1, 2, 3, 4]
    """
    return [int(n) for n in str(i)]
