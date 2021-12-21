from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product
from typing import Literal, TypeAlias, cast

from part1 import read

PlayerIndex: TypeAlias = Literal[0, 1]


def outcomes(rolls: int = 3):
    values = (1, 2, 3)
    for o in product(*(values for _ in range(rolls))):
        yield sum(o)


def outcome_distribution():
    counter = Counter()
    for outcome in outcomes(3):
        counter[outcome] += 1

    return counter


def other(player: PlayerIndex) -> PlayerIndex:
    return cast(PlayerIndex, 1 - player)


def advance(position: int, roll: int) -> int:
    new_position = (position + roll) % 10
    if new_position == 0:
        return 10
    return new_position


DISTRIBUTION = outcome_distribution()


@dataclass
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

    def won(self) -> PlayerIndex | None:
        if self.score[0] >= 21:
            return 0

        if self.score[1] >= 21:
            return 1

        return None


def _traverse(
    state: GameState,
    counter: Counter[PlayerIndex],
    player: PlayerIndex,
    universes: int,
):
    if counter is None:
        counter = Counter()

    winner = state.won()
    if winner is not None:
        counter[winner] += universes
        return

    for roll, u in DISTRIBUTION.items():
        _traverse(state.roll(player, roll), counter, other(player), u * universes)


def traverse(state: GameState):
    counter = Counter()
    _traverse(state, counter, player=0, universes=1)
    return counter


if __name__ == "__main__":
    position = cast(tuple[PlayerIndex, PlayerIndex], tuple(read()))
    print(max(traverse(GameState(position)).values()))
