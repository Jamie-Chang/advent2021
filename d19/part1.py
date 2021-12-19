from __future__ import annotations

import itertools
from dataclasses import astuple, dataclass, field
from typing import Iterable, Iterator, cast

import parse


@dataclass(frozen=True, slots=True)
class Vector:
    x: int
    y: int
    z: int

    def __iter__(self):
        return iter(astuple(self))

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)


@dataclass
class Scanner:
    origin: Vector = Vector(0, 0, 0)
    beacons: set[Vector] = field(default_factory=set)

    def __hash__(self) -> int:
        return id(self)

    def align(self, against: Scanner) -> bool:
        for orientation in orientations(self.beacons):
            for p, other in itertools.product(orientation, against.beacons):
                candidate_origin = other - p
                candidate = reorigin(orientation, candidate_origin)
                if sum(1 for p in candidate if p in against.beacons) < 12:
                    continue

                self.beacons = candidate
                self.origin += candidate_origin
                return True

        return False


def reorigin(beacons: set[Vector], new_origin: Vector):
    return set(p + new_origin for p in beacons)


def _face_rotations(x, y, z):
    yield Vector(x, y, z)
    yield Vector(-y, x, z)
    yield Vector(-x, -y, z)
    yield Vector(y, -x, z)


def _position_orientations(position: Vector) -> Iterator[Vector]:
    x, y, z = position
    yield from _face_rotations(x, y, z)
    yield from _face_rotations(y, x, -z)
    yield from _face_rotations(z, x, y)
    yield from _face_rotations(x, z, -y)
    yield from _face_rotations(y, z, x)
    yield from _face_rotations(z, y, -x)


def orientations(positions: Iterable[Vector]) -> Iterator[set[Vector]]:
    for new in zip(*(_position_orientations(position) for position in positions)):
        yield set(new)


HEADER = parse.compile("--- scanner {scanner:d} ---")
POSITION = parse.compile("{x:d},{y:d},{z:d}")


def read():
    with open("d19/input.txt") as f:
        for line in f:
            yield line.strip()


def parse_scanners(lines: Iterable[str]) -> Iterator[Scanner]:
    scanner: Scanner | None = None
    for line in lines:
        if not line:
            continue

        if HEADER.parse(line):
            if scanner:
                yield scanner
            scanner = Scanner()
            continue

        result = cast(parse.Result, POSITION.parse(line))
        assert scanner is not None
        scanner.beacons.add(Vector(result["x"], result["y"], result["z"]))

    if scanner:
        yield scanner


def align_all(scanners: Iterable[Scanner]) -> None:
    """Align all scanners using breath first traversal."""
    unaligned = set(scanners)
    queue = [unaligned.pop()]
    while queue:
        against = queue.pop()
        aligned = set()
        for scanner in unaligned:
            if scanner.align(against):
                queue.append(scanner)
                aligned.add(scanner)

        unaligned -= aligned


if __name__ == "__main__":
    scanners = list(parse_scanners(read()))
    align_all(scanners)
    print(len(set(itertools.chain(*(scanner.beacons for scanner in scanners)))))
