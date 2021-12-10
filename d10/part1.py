from typing import Final, Iterable, Iterator


CLOSER: Final[dict[str, str]] = {
    "{": "}",
    "(": ")",
    "<": ">",
    "[": "]",
}


SCORES: Final[dict[str, int]] = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def read() -> Iterator[str]:
    with open("d10/input.txt") as f:
        for line in f:
            yield line.strip()


def check(line: str) -> str | None:
    """
    >>> check("()")
    >>> check("(]")
    ']'
    >>> check("(")
    >>> check("]")
    ']'
    """
    stack = []
    for c in line:
        match c, stack:
            case ("{", _) | ("(", _) | ("<", _) | ("[", _):
                stack.append(c)
            case c, []:
                return c
            case c, [*_, opener] if c == CLOSER[opener]:
                stack.pop()
            case c, [*_, opener] if c != CLOSER[opener]:
                return c
    
    return None


def get_scores(lines: Iterable[str]) -> Iterator[int]:
    for line in lines:
        character = check(line)
        if character is None:
            continue

        yield SCORES[character]


if __name__ == "__main__":
    print(sum(get_scores(read())))
