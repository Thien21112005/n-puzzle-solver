"""State of one game: the board, the move count and the solver playback."""

from dataclasses import dataclass

from npuzzle.core.board import DEFAULT_SIZE, State, apply_move, goal_state, random_state
from npuzzle.core.solvers import ALGORITHMS, solve

PLAYBACK_DELAY_MS = 200


@dataclass(frozen=True)
class RunRecord:
    board_id: int
    algorithm: str
    nodes: int
    steps: int
    seconds: float
    memory_estimate: int


class GameSession:
    def __init__(self, size: int = DEFAULT_SIZE):
        self.size = size
        self.goal = goal_state(size)
        self.algorithm = next(iter(ALGORITHMS))
        self.records: list[RunRecord] = []
        self._board_ids: dict[State, int] = {}
        self.solving = False
        self.solution: list[str] = []
        self._last_step_ms = 0
        self.shuffle()

    def scramble(self) -> None:
        self.state = random_state(self.size)
        self.initial_state = self.state

    def shuffle(self) -> None:
        self.scramble()
        self.moves = 0
        self.won = False

    def reset(self) -> None:
        self.state = self.initial_state
        self.moves = 0
        self.won = False
        self.solving = False
        self.solution = []

    def move(self, direction: str) -> None:
        if self.won:
            return
        next_state = apply_move(self.state, direction)
        if next_state is not None:
            self.state = next_state
            self.moves += 1

    def start_solving(self) -> RunRecord | None:
        """Search for a solution and start playing it back."""
        board_id = self._board_ids.setdefault(self.state, len(self._board_ids) + 1)
        result = solve(self.algorithm, self.state, self.goal)
        self.moves = 0
        if result.path is None:
            return None
        self.solving = True
        self.solution = result.path
        record = RunRecord(
            board_id,
            self.algorithm,
            result.nodes,
            len(result.path),
            result.seconds,
            result.memory_estimate,
        )
        self.records.append(record)
        return record

    def update(self, now_ms: int) -> None:
        if self.state == self.goal:
            self.won = True
            self.solving = False
        if self.solving and self.solution and now_ms - self._last_step_ms > PLAYBACK_DELAY_MS:
            self.move(self.solution.pop(0))
            self._last_step_ms = now_ms
            if not self.solution:
                self.solving = False
