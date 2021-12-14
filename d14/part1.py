from typing import Iterable, Iterator, cast

import parse

RULE_FORMAT = parse.compile("{:w} -> {:w}")


def read() -> Iterator[str]:
    with open("d14/input.txt") as f:
        for line in f:
            yield line.strip()


def parse_template(lines: Iterator[str]) -> str:
    template = next(lines)
    next(lines)
    return template


def parse_rules(lines: Iterator[str]) -> Iterable[tuple[str, str]]:
    for line in lines:
        result = cast(parse.Result, RULE_FORMAT.parse(line))
        yield result[0], result[1]


def _step(polymer: str, rules: dict[str, str]) -> Iterator[str]:
    yield polymer[0]
    for a, b in zip(polymer, polymer[1:]):
        insert = rules[a + b]
        yield insert
        yield b


def step(polymer: str, rules: dict[str, str]) -> str:
    return "".join(_step(polymer, rules))


def count(polymer: str) -> dict[str, int]:
    counts = {}
    for c in polymer:
        if c not in counts:
            counts[c] = 0

        counts[c] += 1
    return counts


def amplitude(element_count: dict[str, int]) -> int:
    return max(element_count.values()) - min(element_count.values())


if __name__ == "__main__":
    lines = read()
    polymer = parse_template(lines)
    rules = dict(parse_rules(lines))

    for _ in range(10):
        polymer = step(polymer, rules)

    print(amplitude(count(polymer)))
