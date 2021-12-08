import asyncio
from typing import AsyncIterable, AsyncIterator, Iterable, Iterator

from d8 import constraint
from d8.constraint import Value


def read() -> Iterator[str]:
    with open("d8/input.txt") as f:
        for line in f:
            yield line.strip()


def sort_string(string: str) -> str:
    """
    >>> sort_string("kjldsk")
    'djkkls'
    """
    return "".join(sorted(string))


def parse(lines: Iterable[str]) -> Iterator[tuple[list[str], list[str]]]:
    for line in lines:
        patterns, output = line.split(" | ")
        yield (
            [sort_string(p) for p in patterns.split(" ")],
            [sort_string(o) for o in output.split(" ")],
        )


async def deduce(values: list[Value]) -> dict[str, int]:
    """Resolve all constraints using the event loop.

    The event loop is used to solve constraints that are dependent on
    another value. Allowing the task to be done implicitly in a
    topological order.
    """
    await asyncio.gather(
        # NOTE: Declare constraints here.
        constraint.length(values[0], 6),
        constraint.length(values[1], 2),
        constraint.length(values[3], 5),
        constraint.length(values[4], 4),
        constraint.length(values[5], 5),
        constraint.length(values[6], 6),
        constraint.length(values[7], 3),
        constraint.length(values[8], 7),
        constraint.length(values[9], 6),
        constraint.unique(*values),
        constraint.subsets(values[0], values[8]),
        constraint.subsets(values[1], values[0]),
        constraint.subsets(values[1], values[3]),
        constraint.subsets(values[1], values[4]),
        constraint.subsets(values[1], values[7]),
        constraint.subsets(values[1], values[8]),
        constraint.subsets(values[1], values[9]),
        constraint.subsets(values[2], values[8]),
        constraint.subsets(values[3], values[8]),
        constraint.subsets(values[3], values[9]),
        constraint.subsets(values[4], values[8]),
        constraint.subsets(values[4], values[9]),
        constraint.subsets(values[5], values[8]),
        constraint.subsets(values[5], values[6]),
        constraint.subsets(values[6], values[8]),
        constraint.subsets(values[7], values[0]),
        constraint.subsets(values[7], values[3]),
        constraint.subsets(values[7], values[8]),
        constraint.subsets(values[7], values[9]),
        constraint.subsets(values[9], values[8]),
    )
    return {await value: value.index for value in values}


async def decode(lines: Iterable[str]) -> AsyncIterator[int]:
    for patterns, outputs in parse(lines):
        mapping = await deduce([Value(i, set(patterns)) for i in range(10)])
        yield int("".join(str(mapping[output]) for output in outputs))


async def asum(ai: AsyncIterable[int]) -> int:
    total = 0
    async for i in ai:
        total += i
    return total


async def main() -> None:
    print(await asum(decode(read())))


if __name__ == "__main__":
    asyncio.run(main())
