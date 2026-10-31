# Product

<!-- impeccable:product-schema 1 -->

## Platform

desktop

## Users

Three audiences use the same screen:

- A player who wants to solve the puzzle by hand, with numbers or with their own picture.
- A student presenting or studying search algorithms, who runs several algorithms on one board and compares the results.
- A visitor to the GitHub repository or the author's CV, who judges the project from the app and its screenshots.

## Product Purpose

A 3×3 sliding puzzle that can be played by hand or solved automatically. It makes the differences between search algorithms visible on the same board. Success means a player can finish a game comfortably, and a presenter can show why one algorithm beats another without reading a console.

## Positioning

The same board is both a game and a live comparison: every run of BFS, DFS, UCS, A* or Greedy is recorded against the board it solved, then played back move by move.

## Operating Context

Windows desktop window, run from source or as a single executable. Used with mouse and arrow keys, sometimes on a projector during a presentation.

## Capabilities and Constraints

- Built with Python and pygame; the window is a fixed size and system file dialogs come from tkinter.
- Boards are 3×3. The core accepts other sizes, but the interface does not offer them.
- Algorithms: BFS, DFS, UCS, A*, Greedy, run in the background and cancellable.
- DFS solutions are usually tens of thousands of moves, so playback can be skipped.
- Picture mode cuts a user-chosen picture into tiles and shows the finished picture for reference.
- The interface is available in Vietnamese and English, chosen in settings. Vietnamese is the default.
- Memory figures are estimates (200 bytes per state) and must be labelled as estimates.

## Evidence on Hand

Only figures measured by the app itself may be shown. No benchmarks, user counts or testimonials exist.

## Product Principles

- The board comes first: playing never competes with the comparison.
- Show real measurements, and label what is an estimate.
- Long waits stay visible and can be cancelled or skipped.
- Every label exists in both languages and fits in both.
