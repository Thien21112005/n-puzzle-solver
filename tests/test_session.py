import time

from npuzzle.core.board import apply_move, goal_state, random_state
from npuzzle.core.session import GameSession

GOAL = goal_state(3)
ONE_MOVE_AWAY = apply_move(GOAL, "down")
UNSOLVABLE = (2, 1, 3, 4, 5, 6, 7, 8, 0)


def session_at(state) -> GameSession:
    session = GameSession()
    session.state = state
    session.initial_state = state
    session.moves = 0
    session.won = False
    return session


def wait_for_search(session: GameSession) -> None:
    deadline = time.monotonic() + 30
    while session.searching:
        assert time.monotonic() < deadline
        session.update(0)
        time.sleep(0.001)


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
    assert session.solved_by is None
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
    session.start_solving()
    assert session.solving
    wait_for_search(session)
    assert session.records[-1].steps == 1
    session.update(1000)
    session.update(2000)
    assert session.state == GOAL
    assert session.won
    assert session.solved_by == "BFS"
    assert not session.solving


def test_records_share_an_id_for_the_same_board():
    session = session_at(ONE_MOVE_AWAY)
    session.start_solving()
    wait_for_search(session)
    session.reset()
    session.algorithm = "A*"
    session.start_solving()
    wait_for_search(session)
    assert session.records[0].board_id == session.records[1].board_id
    assert len(session.records) == 2


def test_cancel_stops_the_search_and_keeps_the_board():
    session = session_at(random_state(3))
    board = session.state
    session.start_solving()
    job = session._job
    session.cancel_solving()
    job.join(timeout=5)
    assert not job.is_alive()
    assert not session.solving
    assert not session.searching
    assert session.state == board
    session.update(0)
    assert session.records == []


def test_shuffle_after_winning_unlocks_the_board():
    session = session_at(GOAL)
    session.update(0)
    assert session.won
    session.shuffle()
    assert not session.won
    assert session.moves == 0
    session.update(0)
    assert not session.won


def test_shuffle_during_playback_drops_the_old_solution():
    session = session_at(ONE_MOVE_AWAY)
    session.start_solving()
    wait_for_search(session)
    session.shuffle()
    board = session.state
    assert not session.solving
    assert session.solution == []
    session.update(5000)
    assert session.state == board


def test_skip_to_end_lands_on_the_goal_and_counts_the_moves():
    session = session_at(random_state(3))
    session.algorithm = "DFS"
    session.start_solving()
    wait_for_search(session)
    steps = len(session.solution)
    session.skip_to_end()
    session.update(0)
    assert session.state == GOAL
    assert session.moves == steps
    assert session.won
    assert not session.solving


def test_comparison_keeps_latest_run_per_algorithm_until_shuffle():
    session = session_at(ONE_MOVE_AWAY)
    assert session.comparison() == {}
    for algorithm in ("BFS", "A*", "BFS"):
        session.reset()
        session.algorithm = algorithm
        session.start_solving()
        wait_for_search(session)
    assert set(session.comparison()) == {"BFS", "A*"}
    assert session.comparison()["BFS"] is session.records[-1]
    session.shuffle()
    assert session.comparison() == {}


def test_solving_again_after_a_solver_win_reuses_the_same_board():
    session = session_at(ONE_MOVE_AWAY)
    session.start_solving()
    wait_for_search(session)
    session.skip_to_end()
    session.update(0)
    assert session.won

    session.algorithm = "A*"
    session.start_solving()
    assert session.state == ONE_MOVE_AWAY
    assert not session.won
    wait_for_search(session)
    assert set(session.comparison()) == {"BFS", "A*"}


def test_player_win_does_not_allow_solving_again():
    session = session_at(ONE_MOVE_AWAY)
    session.move("up")
    session.update(0)
    session.start_solving()
    assert not session.solving
    assert session.state == GOAL


def test_cancelling_playback_restores_the_compared_board():
    session = session_at(apply_move(ONE_MOVE_AWAY, "right"))
    start = session.state
    session.start_solving()
    wait_for_search(session)
    session.update(1000)
    assert session.state != start
    session.cancel_solving()
    assert session.state == start
    assert session.moves == 0


def test_unsolvable_board_reports_no_solution():
    session = session_at(UNSOLVABLE)
    session.start_solving()
    wait_for_search(session)
    assert session.no_solution
    assert not session.solving
