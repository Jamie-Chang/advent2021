from statistics import median
from typing import Final, Iterable, Iterator


CLOSER: Final[dict[str, str]] = {
    "{": "}",
    "(": ")",
    "<": ">",
    "[": "]",
}


SCORES: Final[dict[str, int]] = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def read() -> Iterator[str]:
    with open("d10/input.txt") as f:
        for line in f:
            yield line.strip()


def complete(line: str) -> str | None:
    """
    >>> complete("()")
    ''
    >>> complete("(]")
    >>> complete("(")
    ')'
    >>> complete("]")
    """
    stack = []
    for c in line:
        match c, stack:
            case ("{", _) | ("(", _) | ("<", _) | ("[", _):
                stack.append(c)
            case c, []:
                return None
            case c, [*_, opener] if c == CLOSER[opener]:
                stack.pop()
            case c, [*_, opener] if c != CLOSER[opener]:
                return None

    return "".join(CLOSER[opener] for opener in reversed(stack))


def get_score(completion: str) -> int:
    """
    >>> get_score("])}>")
    294
    """
    score = 0
    for c in completion:
        score *= 5
        score += SCORES[c]

    return score


def get_scores(lines: Iterable[str]) -> Iterator[int]:
    for line in lines:
        completion = complete(line)
        if completion is None:
            continue

        yield get_score(completion)


if __name__ == "__main__":
    print(median(get_scores(read())))
