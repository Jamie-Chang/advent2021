from typing import Hashable, Iterable, Iterator, TypeVar


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


def index_on_length(patterns: list[str]) -> dict[int, list[str]]:
    """
    >>> index_on_length(['abcd', 'cde', 'agd'])
    {4: ['abcd'], 3: ['cde', 'agd']}
    """
    length_index = {}
    for pattern in patterns:
        length_index.setdefault(len(pattern), []).append(pattern)

    return length_index


def subset(pattern1: str, pattern2: str) -> bool:
    """
    >>> subset('bc', 'cba')
    True
    >>> subset('cba', 'cad')
    False
    """
    return set(pattern1).issubset(set(pattern2))


def deduce(patterns: list[str]) -> dict[int, str]:
    """
    >>> mapping = deduce([
    ...     "acedgfb",
    ...     "cdfbe",
    ...     "gcdfa",
    ...     "fbcad",
    ...     "dab",
    ...     "cefabd",
    ...     "cdfgeb",
    ...     "eafb",
    ...     "cagedb",
    ...     "ab",
    ... ])
    >>> mapping == {
    ...     8: "acedgfb",
    ...     5: "cdfbe",
    ...     2: "gcdfa",
    ...     3: "fbcad",
    ...     7: "dab",
    ...     9: "cefabd",
    ...     6: "cdfgeb",
    ...     4: "eafb",
    ...     0: "cagedb",
    ...     1: "ab",
    ... }
    True
    """
    length = index_on_length(patterns)

    mapping: dict[int, str] = {
        1: length[2][0],
        4: length[4][0],
        7: length[3][0],
        8: length[7][0],
    }

    for pattern in length[5]:
        if subset(mapping[7], pattern):
            mapping[3] = pattern

    for pattern in length[6]:
        if subset(mapping[3], pattern):
            mapping[9] = pattern
        elif subset(mapping[1], pattern):
            mapping[0] = pattern
        else:
            mapping[6] = pattern

    for pattern in length[5]:
        if pattern is mapping[3]:
            continue
        elif subset(pattern, mapping[6]):
            mapping[5] = pattern
        else:
            mapping[2] = pattern

    return mapping


T = TypeVar("T", bound=Hashable)
S = TypeVar("S", bound=Hashable)


def inverse(dictionary: dict[T, S]) -> dict[S, T]:
    return {v: k for k, v in dictionary.items()}


def decode(lines: Iterable[str]) -> Iterator[int]:
    for patterns, outputs in parse(lines):
        mapping = inverse(deduce(patterns))

        yield int("".join(str(mapping[output]) for output in outputs))


if __name__ == "__main__":
    print(sum(decode(read())))
