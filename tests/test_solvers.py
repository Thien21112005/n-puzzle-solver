import random

import pytest

from npuzzle.core.board import apply_move, goal_state, neighbors
from npuzzle.core.solvers import solve

GOAL = goal_state(3)
UNSOLVABLE = (2, 1, 3, 4, 5, 6, 7, 8, 0)


def scrambled(seed: int, steps: int = 40):
    """Walk away from the goal, so the board is always solvable."""
    rng = random.Random(seed)
    state = GOAL
    for _ in range(steps):
        state = rng.choice(list(neighbors(state)))[1]
    return state


def replay(state, path):
    for direction in path:
        state = apply_move(state, direction)
        assert state is not None
    return state


@pytest.mark.parametrize("algorithm", ["BFS", "UCS", "A*", "Greedy"])
@pytest.mark.parametrize("seed", range(3))
def test_solution_reaches_the_goal(algorithm, seed):
    start = scrambled(seed)
    result = solve(algorithm, start, GOAL)
    assert replay(start, result.path) == GOAL
    assert result.nodes > 0
    assert result.seconds >= 0
    assert result.memory_estimate > 0


@pytest.mark.parametrize("algorithm", ["BFS", "UCS", "A*", "Greedy"])
def test_goal_state_needs_no_moves(algorithm):
    assert solve(algorithm, GOAL, GOAL).path == []


def test_unsolvable_board_reports_no_path():
    assert solve("A*", UNSOLVABLE, GOAL).path is None
