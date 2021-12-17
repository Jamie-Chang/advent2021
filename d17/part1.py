from typing import cast
from parse import Result, parse


def read() -> tuple[tuple[int, int], tuple[int, int]]:
    with open("d17/input.txt") as f:
        result = parse("target area: x={x0:d}..{x1:d}, y={y0:d}..{y1:d}", f.read())
        result = cast(Result, result)
        return (result["x0"], result["x1"]), (result["y0"], result["y1"])


def apogee(initial: int) -> int:
    """
    >>> apogee(9)
    45
    """
    if initial < 0:
        return 0

    return position(initial, steps=initial + 1)


def position(initial: int, steps: int) -> int:
    """
    >>> position(9, 10)
    45
    >>> position(9, 9)
    45
    >>> position(2, 4)
    2
    >>> position(2, 6)
    -3
    >>> position(-4, 2)
    -9
    """
    return (initial + (initial - steps + 1)) * steps // 2


if __name__ == "__main__":
    _, (y0, _) = read()
    # NOTE: At 0 height, the velocity is -initial - 1
    # Best toss is -(y0 + 1)
    print(apogee(-y0 - 1))
