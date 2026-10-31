"""Search algorithms for the sliding puzzle, sharing one search loop."""

import heapq
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from itertools import count

from npuzzle.core.board import State, manhattan, neighbors

ESTIMATED_BYTES_PER_STATE = 200


@dataclass(frozen=True)
class SolveResult:
    path: list[str] | None
    nodes: int
    seconds: float
    memory_estimate: int


class _QueueFrontier:
    def __init__(self):
        self._items = deque()

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.popleft()

    def __len__(self):
        return len(self._items)


class _StackFrontier(_QueueFrontier):
    def pop(self):
        return self._items.pop()


class _PriorityFrontier:
    def __init__(self, priority: Callable[[int, State], int]):
        self._priority = priority
        self._items = []
        self._order = count()

    def push(self, item):
        cost, state, _ = item
        heapq.heappush(self._items, (self._priority(cost, state), next(self._order), item))

    def pop(self):
        return heapq.heappop(self._items)[-1]

    def __len__(self):
        return len(self._items)


def _search(start: State, goal: State, frontier) -> SolveResult:
    started = time.perf_counter()
    frontier.push((0, start, []))
    visited = {start}
    largest_frontier = 1

    while len(frontier):
        largest_frontier = max(largest_frontier, len(frontier))
        cost, state, path = frontier.pop()
        if state == goal:
            memory = (largest_frontier + len(visited)) * ESTIMATED_BYTES_PER_STATE
            return SolveResult(path, len(visited), time.perf_counter() - started, memory)
        for direction, next_state in neighbors(state):
            if next_state not in visited:
                visited.add(next_state)
                frontier.push((cost + 1, next_state, path + [direction]))

    return SolveResult(None, 0, time.perf_counter() - started, 0)


def _breadth_first(start: State, goal: State) -> SolveResult:
    return _search(start, goal, _QueueFrontier())


def _depth_first(start: State, goal: State) -> SolveResult:
    return _search(start, goal, _StackFrontier())


def _uniform_cost(start: State, goal: State) -> SolveResult:
    return _search(start, goal, _PriorityFrontier(lambda cost, _: cost))


def _a_star(start: State, goal: State) -> SolveResult:
    return _search(start, goal, _PriorityFrontier(lambda cost, state: cost + manhattan(state)))


def _greedy(start: State, goal: State) -> SolveResult:
    return _search(start, goal, _PriorityFrontier(lambda _, state: manhattan(state)))


ALGORITHMS: dict[str, Callable[[State, State], SolveResult]] = {
    "BFS": _breadth_first,
    "DFS": _depth_first,
    "UCS": _uniform_cost,
    "A*": _a_star,
    "Greedy": _greedy,
}


def solve(algorithm: str, start: State, goal: State) -> SolveResult:
    return ALGORITHMS[algorithm](start, goal)
