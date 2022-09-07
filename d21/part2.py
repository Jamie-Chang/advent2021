from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import cache, cached_property
from itertools import product
from typing import Literal, TypeAlias, cast

from part1 import read

PlayerIndex: TypeAlias = Literal[0, 1]


def outcomes(rolls: int = 3):
    values = (1, 2, 3)
    for o in product(*(values for _ in range(rolls))):
        yield sum(o)


def other(player: PlayerIndex) -> PlayerIndex:
    return cast(PlayerIndex, 1 - player)


def advance(position: int, roll: int) -> int:
    new_position = (position + roll) % 10
    if new_position == 0:
        return 10
    return new_position


DISTRIBUTION = Counter(outcomes(3))


@dataclass(frozen=True)
class GameState:
    position: tuple[int, int]

    score: tuple[int, int] = 0, 0

    def roll(self, player: PlayerIndex, value: int) -> GameState:
        new_position = advance(self.position[player], value)
        new_score = self.score[player] + new_position
        if player == 0:
            return GameState(
                position=(new_position, self.position[1]),
                score=(new_score, self.score[1]),
            )

        return GameState(
            position=(self.position[0], new_position),
            score=(self.score[0], new_score),
        )

    @cached_property
    def winner(self, score: int = 21) -> PlayerIndex | None:
        if self.score[0] >= score:
            return 0

        if self.score[1] >= score:
            return 1

        return None


@cache
def traverse(state: GameState, player: PlayerIndex = 0, universes: int = 1):
    if state.winner is not None:
        return Counter({state.winner: universes})

    result = Counter()
    for roll, u in DISTRIBUTION.items():
        result += traverse(state.roll(player, roll), other(player), u * universes)
    return result


if __name__ == "__main__":
    position = cast(tuple[PlayerIndex, PlayerIndex], tuple(read()))
    print(max(traverse(GameState(position)).values()))
