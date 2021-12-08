"""Solution using a declarative approach.
"""
import asyncio
from asyncio.tasks import FIRST_COMPLETED
from dataclasses import dataclass, field
from itertools import combinations


@dataclass
class Value:
    index: int
    options: set[str]

    resolved: asyncio.Event = field(
        init=False, repr=False, default_factory=asyncio.Event
    )

    async def remove(self, options: set[str]) -> None:
        self.options -= options
        assert self.options, "Something is wrong with the logic"
        self._check()

    def __await__(self):
        return self.get().__await__()

    async def get(self) -> str:
        await self.resolved.wait()
        return self.result()

    def result(self) -> str:
        assert len(self.options) == 1
        return list(self.options)[0]

    def _check(self) -> None:
        if len(self.options) == 1:
            self.resolved.set()


async def _first_complete(*values: Value) -> Value:
    value_tasks = [asyncio.create_task(v.get()) for v in values]
    done, _ = await asyncio.wait(value_tasks, return_when=FIRST_COMPLETED)
    for i, task in enumerate(value_tasks):
        if task in done:
            for task in value_tasks:
                task.cancel()
            return values[i]
    assert False


def _subset(pattern1: str, pattern2: str) -> bool:
    """
    >>> subset('bc', 'cba')
    True
    >>> subset('cba', 'cad')
    False
    """
    return set(pattern1).issubset(set(pattern2))


async def subsets(sub: Value, sup: Value) -> None:
    """Declare that `value1` ⊆ `values2`."""
    first = await _first_complete(sub, sup)
    if sub is first:
        sub_value = await sub
        remove = {v for v in sup.options if not _subset(sub_value, v)}
        await sup.remove(remove)

    else:
        sup_value = await sup
        remove = {v for v in sub.options if not _subset(v, sup_value)}
        await sub.remove(remove)


async def length(value: Value, n: int) -> None:
    """Declare that the `value` is of length `n`."""
    remove = {v for v in value.options if len(v) != n}
    await value.remove(remove)


async def ne(value1: Value, value2: Value) -> None:
    """Declare that `value1` != `value2`."""
    first = await _first_complete(value1, value2)
    other = value2 if first is value1 else value1
    await other.remove({await first})


async def unique(*values: Value) -> None:
    """Declare that values are unique.

    That is for each pair of values they are not equal to each other.
    """
    await asyncio.gather(*(ne(v1, v2) for v1, v2 in combinations(values, 2)))
