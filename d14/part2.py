from collections import Counter
from typing import Iterable, Iterator, TypeAlias, cast

import parse

RULE_FORMAT = parse.compile("{:w} -> {:w}")

Pair: TypeAlias = str
NewPairs: TypeAlias = set[Pair]
Element: TypeAlias = str


def read() -> Iterator[str]:
    with open("d14/input.txt") as f:
        for line in f:
            yield line.strip()


def parse_template(lines: Iterator[str]) -> str:
    template = next(lines)
    next(lines)
    return template


def parse_rules(lines: Iterator[str]) -> Iterable[tuple[Pair, NewPairs]]:
    for line in lines:
        result = cast(parse.Result, RULE_FORMAT.parse(line))
        yield result[0], {result[0][0] + result[1], result[1] + result[0][1]}


def get_pair_count(template: str) -> Counter[Pair]:
    return Counter(a + b for a, b in zip(template, template[1:]))


def step(pairs: Counter[Pair], rules: dict[Pair, NewPairs]) -> Counter[Pair]:
    counter = Counter()
    for pair, c in pairs.items():
        for new_pair in rules[pair]:
            counter[new_pair] += c
    return counter


def count(pairs: Counter[Pair], start: Element, end: Element) -> Counter[Element]:
    counter = Counter()
    for pair, c in pairs.items():
        for element in pair:
            counter[element] += c

    counter[start] += 1
    counter[end] += 1

    for element in counter:
        element //= 2

    return counter


def amplitude(count: Counter[Element]) -> int:
    return max(count.values()) - min(count.values())


if __name__ == "__main__":
    lines = read()
    polymer = parse_template(lines)
    rules = dict(parse_rules(lines))
    pair_count = get_pair_count(polymer)

    for _ in range(40):
        pair_count = step(pair_count, rules)

    print(amplitude(count(pair_count, start=polymer[0], end=polymer[-1])))
