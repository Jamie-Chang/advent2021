import cmath
import math
from typing import Iterable, Iterator

from part1 import read


def solve_quadratic(a: int, b: int, c: int) -> Iterable[complex]:
    yield (-b + cmath.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    yield (-b - cmath.sqrt(b ** 2 - 4 * a * c)) / (2 * a)


def max_real(solutions: Iterable[complex]) -> float:
    return max(x.real for x in solutions if x.real == x)


def _solve_y_steps(initial: int, position: int) -> float:
    """
    We calculate the position using the following equation:

    position = (initial + (initial - steps + 1)) * steps // 2

    Instead solve for steps given initial and position.
    """
    return max_real(
        solve_quadratic(
            a=1,
            b=-(2 * initial + 1),
            c=position * 2,
        )
    )


def solve_y_steps(initial: int, target_range: tuple[int, int]) -> Iterator[int]:
    """
    >>> list(solve_y_steps(5, -10, -5))
    [12]
    """
    step_low = math.ceil(_solve_y_steps(initial, target_range[1]))
    step_high = math.floor(_solve_y_steps(initial, target_range[0]))
    for step in range(step_low, step_high + 1):
        yield step


def _solve_x_initial(steps: int, position: int):
    """
    We calculate the position using the following equation:

    position = (initial + (initial - steps + 1)) * steps // 2 if steps < initial
    position = (initial + 1) * initial // 2 if steps >= initial

    Solving for initial based on steps and position.
    """
    initial = max_real(solve_quadratic(a=1, b=1, c=-2 * position))
    if steps >= initial:
        return initial

    return (2 * position + steps ** 2 - steps) / (2 * steps)


def solve_x_initial(steps: int, target_low: int, target_high: int) -> Iterator[int]:
    """
    >>> list(solve_x_initial(7, 20, 30))
    [6, 7]
    """

    initial_low = _solve_x_initial(steps, target_low)
    initial_high = _solve_x_initial(steps, target_high)
    for initial in range(math.ceil(initial_low), math.floor(initial_high) + 1):
        yield initial


def solve(target_x: tuple[int, int], target_y: tuple[int, int]):
    # NOTE: From part 1 initial y has to between + lower bound and - lower bound
    for y in range(target_y[0], -target_y[0]):
        for steps in solve_y_steps(y, target_y):
            for x in solve_x_initial(steps, target_x[0], target_x[1]):
                yield x, y


def ilen(iterable: Iterable) -> int:
    return sum(1 for _ in iterable)


if __name__ == "__main__":
    print(len(set(solve(*read()))))
