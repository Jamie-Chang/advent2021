from typing import Iterable

from d16.part1 import Packet, get_bits, parse, read



def product(iterable: Iterable[int], start: int = 1) -> int:
    """
    >>> product([2])
    2
    >>> product([2, 3])
    6
    >>> product([])
    1
    >>> product([2], start=10)
    20
    """
    for v in iterable:
        start *= v

    return start


def evaluate(packet: Packet) -> int:
    match packet:
        case Packet(type_id=0, content=[*content]):
            return sum(evaluate(p) for p in content)

        case Packet(type_id=1, content=[*content]):
            return product(evaluate(p) for p in content)

        case Packet(type_id=2, content=[*content]):
            return min(evaluate(p) for p in content)

        case Packet(type_id=3, content=[*content]):
            return max(evaluate(p) for p in content)

        case Packet(type_id=4, content=value) if isinstance(value, int):
            return value

        case Packet(type_id=5, content=[first, second]):
            return 1 if evaluate(first) > evaluate(second) else 0

        case Packet(type_id=6, content=[first, second]):
            return 1 if evaluate(first) < evaluate(second) else 0

        case Packet(type_id=7, content=[first, second]):
            return 1 if evaluate(first) == evaluate(second) else 0

        case _:
            assert False, f"Invalid {packet = }"


if __name__ == "__main__":
    packet = parse(get_bits(read()))
    assert packet is not None
    print(evaluate(packet))
