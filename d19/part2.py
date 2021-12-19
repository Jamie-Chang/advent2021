import itertools

from part1 import Vector, parse_scanners, read, align_all


def manhattan_distance(v1: Vector, v2: Vector):
    """
    >>> manhattan_distance(Vector(1, 1, 1), Vector(0, 0, 0))
    3
    >>> manhattan_distance(Vector(0, 1, 0), Vector(1, 0, 1))#
    3
    """
    return sum(abs(d) for d in v1 - v2)


if __name__ == "__main__":
    sensors = parse_scanners(read())
    align_all(sensors)
    print(
        max(
            manhattan_distance(*p)
            for p in itertools.combinations((s.origin for s in sensors), 2)
        )
    )
