from itertools import permutations

from part1 import magnitude, parse_one, read


if __name__ == "__main__":
    print(
        max(
            magnitude(
                parse_one(a) + parse_one(b),
            )
            for a, b in permutations(read(), 2)
        )
    )
