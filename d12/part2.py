from typing import Iterable, Iterator, cast

import parse

LINE_FORMAT = parse.compile("{:w}-{:w}")


def read() -> Iterator[str]:
    with open("d12/input.txt") as f:
        for line in f:
            yield line.strip()


def parse_edge(line: str) -> tuple[str, str]:
    """
    >>> parse_edge("abcd-A")
    ('abcd', 'A')
    """
    result = cast(parse.Result, LINE_FORMAT.parse(line))
    return result[0], result[1]


def get_adjacency(lines: Iterable[str]) -> dict[str, set[str]]:
    matrix: dict[str, set[str]] = {}
    for line in lines:
        start, end = parse_edge(line)
        matrix.setdefault(start, set()).add(end)
        matrix.setdefault(end, set()).add(start)

    return matrix


def find_paths(
    adjacency: dict[str, set[str]],
    visited: set[str] | None = None,
    twice: str | None = None,
    start: str = "start",
) -> Iterator[list[str]]:
    if visited is None:
        visited = set()

    if start in visited:
        if start in ("start", "end"):
            return

        if twice is not None:
            return

        twice = start

    if start.islower():
        visited = visited | {start}

    if start == "end":
        yield ["end"]
        return

    for cave in adjacency[start]:
        for path in find_paths(adjacency, visited, twice, cave):
            yield [start] + path


def ilen(it: Iterable) -> int:
    return sum(1 for _ in it)


if __name__ == "__main__":
    print(ilen(find_paths(get_adjacency(read()))))
