from npuzzle.core.board import apply_move, goal_state
from npuzzle.core.session import GameSession

GOAL = goal_state(3)
ONE_MOVE_AWAY = apply_move(GOAL, "down")


def session_at(state) -> GameSession:
    session = GameSession()
    session.state = state
    session.initial_state = state
    session.moves = 0
    session.won = False
    return session


def test_move_counts_only_legal_moves():
    session = session_at(GOAL)
    session.move("up")
    assert session.moves == 0
    session.move("down")
    assert session.moves == 1


def test_reaching_the_goal_wins_and_blocks_moves():
    session = session_at(ONE_MOVE_AWAY)
    session.move("up")
    session.update(0)
    assert session.won
    session.move("down")
    assert session.state == GOAL


def test_reset_restores_the_initial_board():
    session = session_at(ONE_MOVE_AWAY)
    session.move("up")
    session.update(0)
    session.reset()
    assert session.state == ONE_MOVE_AWAY
    assert session.moves == 0
    assert not session.won


def test_solver_playback_finishes_on_the_goal():
    session = session_at(ONE_MOVE_AWAY)
    record = session.start_solving()
    assert record.steps == 1
    session.update(1000)
    session.update(2000)
    assert session.state == GOAL
    assert session.won
    assert not session.solving


def test_records_share_an_id_for_the_same_board():
    session = session_at(ONE_MOVE_AWAY)
    first = session.start_solving()
    session.reset()
    session.algorithm = "A*"
    second = session.start_solving()
    assert first.board_id == second.board_id
    assert len(session.records) == 2
