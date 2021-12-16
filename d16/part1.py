import itertools
from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass
class Packet:
    version: int
    type_id: int
    content: list["Packet"] | int

    def versions(self) -> Iterator[int]:
        yield self.version
        if isinstance(self.content, list):
            for packet in self.content:
                yield from packet.versions()


def read() -> str:
    with open("d16/input.txt") as f:
        return f.read().strip()


def get_bits(hex: str) -> Iterator[str]:
    """
    >>> list(get_bits('A'))
    ['1', '0', '1', '0']
    >>> list(get_bits('1'))
    ['0', '0', '0', '1']
    """
    for h in hex:
        d = int(h, base=16)
        for b in f"{d:04b}":
            yield b


def take(bits: Iterable[str], number: int) -> str:
    """
    >>> take('11000001', 2)
    '11'
    >>> take('110', 4)
    '110'
    """
    took = "".join(itertools.islice(bits, number))
    return took


def _parse_hex_digits(bits: Iterator[str]) -> Iterator[str]:
    while True:
        number = take(bits, 5)
        yield number[1:]
        if number[0] == "0":
            return


def parse_number(bits: Iterable[str]) -> int:
    """
    >>> bits = iter('101111111000101000')
    >>> parse_number(bits)
    2021
    """
    bits = iter(bits)  # NOTE: Ensure that it is an iterator
    return int("".join(_parse_hex_digits(bits)), base=2)


def parse(bits: Iterable[str]) -> Packet | None:
    bits = iter(bits)
    headers = take(bits, 6)
    if not headers:
        return None

    version = int(headers[:3], base=2)
    type_id = int(headers[-3:], base=2)

    if type_id == 4:
        return Packet(version, type_id, content=parse_number(bits))

    length_type_id = int(take(bits, 1))

    if length_type_id == 0:
        return Packet(
            version,
            type_id,
            content=list(
                parse_until_length(
                    bits,
                    length=int(take(bits, 15), base=2),
                )
            ),
        )

    return Packet(
        version,
        type_id,
        content=list(
            parse_until_limit(
                bits,
                limit=int(take(bits, 11), base=2),
            )
        ),
    )


def parse_until_length(bits: Iterable[str], length: int) -> Iterator[Packet]:
    bits = iter(take(bits, length))
    while packet := parse(bits):
        yield packet


def parse_until_limit(bits: Iterable[str], limit: int) -> Iterator[Packet]:
    bits = iter(bits)
    for _ in range(limit):
        packet = parse(bits)
        assert packet is not None
        yield packet


if __name__ == "__main__":
    packet = parse(get_bits(read()))
    assert packet is not None
    print(sum(packet.versions()))
