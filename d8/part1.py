from typing import Iterable, Iterator


def read() -> Iterator[str]:
    with open("d8/input.txt") as f:
        for line in f:
            yield line.strip()


def parse(lines: Iterable[str]) -> Iterator[tuple[list[str], list[str]]]:
    for line in lines:
        patterns, output = line.split(' | ')
        yield patterns.split(' '), output.split(' ')


def count_digits(lines: Iterable[str]) -> int:
    count = 0
    for _, outputs in parse(lines):
        for output in outputs:
            if len(output) in (2, 4, 3, 7):
                count += 1

    return count


if __name__ == "__main__":
    print(count_digits(read()))
