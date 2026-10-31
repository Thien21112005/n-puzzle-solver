"""State of one game: the board, the move count and the solver playback."""

import threading
from dataclasses import dataclass

from npuzzle.core.board import DEFAULT_SIZE, State, apply_move, goal_state, random_state
from npuzzle.core.solvers import ALGORITHMS, SolveResult, solve

PLAYBACK_DELAY_MS = 200


@dataclass(frozen=True)
class RunRecord:
    board_id: int
    algorithm: str
    nodes: int
    steps: int
    seconds: float
    memory_estimate: int


class _SearchJob(threading.Thread):
    """Run one search away from the interface thread so the window stays responsive."""

    def __init__(self, algorithm: str, start: State, goal: State):
        super().__init__(daemon=True)
        self.algorithm = algorithm
        self.board = start
        self.goal = goal
        self.result: SolveResult | None = None
        self._cancel_event = threading.Event()

    def run(self) -> None:
        self.result = solve(self.algorithm, self.board, self.goal, self._cancel_event.is_set)

    def cancel(self) -> None:
        self._cancel_event.set()


class GameSession:
    def __init__(self, size: int = DEFAULT_SIZE):
        self.size = size
        self.goal = goal_state(size)
        self.algorithm = next(iter(ALGORITHMS))
        self.records: list[RunRecord] = []
        self._board_ids: dict[State, int] = {}
        self._compared_board: int | None = None
        self.solving = False
        self.no_solution = False
        self.solved_by: str | None = None
        self._solve_start: State | None = None
        self.solution: list[str] = []
        self._job: _SearchJob | None = None
        self._last_step_ms = 0
        self.shuffle()

    @property
    def searching(self) -> bool:
        return self._job is not None

    def comparison(self) -> dict[str, RunRecord]:
        """Return the latest run of each algorithm on the board solved last."""
        return {r.algorithm: r for r in self.records if r.board_id == self._compared_board}

    def shuffle(self) -> None:
        self.cancel_solving()
        self._compared_board = None
        self.state = random_state(self.size)
        self.initial_state = self.state
        self.moves = 0
        self.won = False

    def reset(self) -> None:
        self.cancel_solving()
        self.state = self.initial_state
        self.moves = 0
        self.won = False

    def move(self, direction: str) -> None:
        if self.won:
            return
        next_state = apply_move(self.state, direction)
        if next_state is not None:
            self.state = next_state
            self.moves += 1

    def start_solving(self) -> None:
        """Start searching for a solution; update() begins the playback when it is found."""
        if self.solving or (self.won and not self.solved_by):
            return
        if self.won:
            # A solver finished this board: run the next algorithm on the same one.
            self.state = self._solve_start
            self.won = False
        self._solve_start = self.state
        self.solved_by = None
        self.moves = 0
        self.no_solution = False
        self.solving = True
        self._job = _SearchJob(self.algorithm, self.state, self.goal)
        self._job.start()

    def cancel_solving(self) -> None:
        if self._job is not None:
            self._job.cancel()
            self._job = None
        if self.solution:
            # Stopping a playback returns to the board the results belong to.
            self.state = self._solve_start
            self.moves = 0
        self.solving = False
        self.no_solution = False
        self.solved_by = None
        self.solution = []

    def skip_to_end(self) -> None:
        """Jump over the remaining playback, which can take hours with DFS."""
        for direction in self.solution:
            self.move(direction)
        self.solution = []
        self.solving = False

    def _finish_search(self) -> None:
        job, self._job = self._job, None
        result = job.result
        if result.path is None:
            self.no_solution = True
            self.solving = False
            return
        self.solution = result.path
        self.solved_by = job.algorithm
        board_id = self._board_ids.setdefault(job.board, len(self._board_ids) + 1)
        self._compared_board = board_id
        self.records.append(
            RunRecord(
                board_id,
                job.algorithm,
                result.nodes,
                len(result.path),
                result.seconds,
                result.memory_estimate,
            )
        )

    def update(self, now_ms: int) -> None:
        if self._job is not None and not self._job.is_alive():
            self._finish_search()
        if self.state == self.goal:
            self.won = True
            self.solving = False
        if self.searching or not self.solving:
            return
        if self.solution and now_ms - self._last_step_ms > PLAYBACK_DELAY_MS:
            self.move(self.solution.pop(0))
            self._last_step_ms = now_ms
        if not self.solution:
            self.solving = False
