import random

import pytest

from npuzzle.core.board import apply_move, goal_state, neighbors
from npuzzle.core.solvers import ALGORITHMS, solve

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


@pytest.mark.parametrize("algorithm", ALGORITHMS)
@pytest.mark.parametrize("seed", range(3))
def test_solution_reaches_the_goal(algorithm, seed):
    start = scrambled(seed)
    result = solve(algorithm, start, GOAL)
    assert replay(start, result.path) == GOAL
    assert result.nodes > 0
    assert result.seconds >= 0
    assert result.memory_estimate > 0


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_goal_state_needs_no_moves(algorithm):
    assert solve(algorithm, GOAL, GOAL).path == []


@pytest.mark.parametrize("seed", range(25))
def test_a_star_and_ucs_match_the_optimal_bfs_length(seed):
    start = scrambled(seed, steps=60)
    optimal = len(solve("BFS", start, GOAL).path)
    assert len(solve("UCS", start, GOAL).path) == optimal
    assert len(solve("A*", start, GOAL).path) == optimal


def test_a_star_explores_fewer_states_than_bfs():
    start = scrambled(7, steps=60)
    assert solve("A*", start, GOAL).nodes < solve("BFS", start, GOAL).nodes


def test_stop_check_ends_the_search_early():
    result = solve("BFS", scrambled(1), GOAL, should_stop=lambda: True)
    assert result.path is None


def test_unsolvable_board_reports_no_path():
    assert solve("A*", UNSOLVABLE, GOAL).path is None
