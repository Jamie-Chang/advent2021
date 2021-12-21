from dataclasses import dataclass
from itertools import cycle
from typing import Iterable, Iterator, cast
import parse

FORMAT = parse.compile("Player {player:d} starting position: {position:d}")


def read() -> Iterator[int]:
    with open("d21/input.txt") as f:
        for line in f:
            yield cast(parse.Result, FORMAT.parse(line.strip()))["position"]


def deterministic_dice():
    return cycle(range(1, 101))


def roll(dice: Iterator[int], times: int = 1) -> int:
    return sum(next(dice) for _ in range(times))


@dataclass
class Player:
    position: int
    score: int = 0

    def play(self, dice: Iterator[int]) -> bool:
        position = (self.position + roll(dice, 3)) % 10
        if position == 0:
            position = 10
        self.score += position
        self.position = position
        return self.score >= 1000


def play(player_starts: Iterable[int]) -> int:
    dice = deterministic_dice()
    players = tuple(Player(p) for p in player_starts)
    for turn, player in enumerate(cycle(players), 1):
        result = player.play(dice)
        other = players[1] if player is players[0] else players[0]
        if result:
            return turn * 3 * other.score

    assert False


if __name__ == "__main__":
    print(play(read()))
