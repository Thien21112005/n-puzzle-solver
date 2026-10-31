"""Rules of the sliding puzzle.

A state is a flat tuple read row by row, with 0 standing for the blank. Move
names describe the direction a tile slides, so "up" moves the tile below the
blank upward.
"""

import random
from collections.abc import Iterator
from math import isqrt

State = tuple[int, ...]

DEFAULT_SIZE = 3
BLANK = 0

_BLANK_OFFSETS = {"up": (1, 0), "down": (-1, 0), "left": (0, 1), "right": (0, -1)}


def goal_state(size: int = DEFAULT_SIZE) -> State:
    return (*range(1, size * size), BLANK)


def is_solvable(state: State) -> bool:
    """Check the inversion parity, which no legal move can change."""
    size = board_size(state)
    tiles = [value for value in state if value != BLANK]
    inversions = sum(
        tiles[i] > tiles[j] for i in range(len(tiles)) for j in range(i + 1, len(tiles))
    )
    if size % 2 == 1:
        return inversions % 2 == 0
    blank_row_from_bottom = size - 1 - state.index(BLANK) // size
    return (inversions + blank_row_from_bottom) % 2 == 0


def random_state(size: int = DEFAULT_SIZE) -> State:
    """Return a solvable board that is not already solved."""
    goal = goal_state(size)
    values = list(goal)
    while True:
        random.shuffle(values)
        state = tuple(values)
        if state != goal and is_solvable(state):
            return state


def board_size(state: State) -> int:
    return isqrt(len(state))


def apply_move(state: State, direction: str) -> State | None:
    """Return the state after the move, or None when the move is not possible."""
    size = board_size(state)
    blank = state.index(BLANK)
    row, col = divmod(blank, size)
    row_offset, col_offset = _BLANK_OFFSETS[direction]
    target_row, target_col = row + row_offset, col + col_offset
    if not (0 <= target_row < size and 0 <= target_col < size):
        return None
    target = target_row * size + target_col
    cells = list(state)
    cells[blank], cells[target] = cells[target], cells[blank]
    return tuple(cells)


def neighbors(state: State) -> Iterator[tuple[str, State]]:
    for direction in _BLANK_OFFSETS:
        next_state = apply_move(state, direction)
        if next_state is not None:
            yield direction, next_state


def manhattan(state: State) -> int:
    """Sum of the distances between each tile and its goal position."""
    size = board_size(state)
    total = 0
    for index, value in enumerate(state):
        if value != BLANK:
            row, col = divmod(index, size)
            goal_row, goal_col = divmod(value - 1, size)
            total += abs(row - goal_row) + abs(col - goal_col)
    return total
