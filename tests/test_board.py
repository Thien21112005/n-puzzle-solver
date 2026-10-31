from npuzzle.core.board import apply_move, goal_state, manhattan, neighbors, random_state


def test_goal_state_puts_blank_last():
    assert goal_state(3) == (1, 2, 3, 4, 5, 6, 7, 8, 0)
    assert goal_state(4)[-1] == 0
    assert len(goal_state(4)) == 16


def test_move_names_describe_the_sliding_tile():
    goal = goal_state(3)
    assert apply_move(goal, "down") == (1, 2, 3, 4, 5, 0, 7, 8, 6)
    assert apply_move(goal, "right") == (1, 2, 3, 4, 5, 6, 7, 0, 8)


def test_move_off_the_board_is_rejected():
    goal = goal_state(3)
    assert apply_move(goal, "up") is None
    assert apply_move(goal, "left") is None


def test_neighbor_count_depends_on_blank_position():
    assert len(list(neighbors((0, 1, 2, 3, 4, 5, 6, 7, 8)))) == 2
    assert len(list(neighbors((1, 0, 2, 3, 4, 5, 6, 7, 8)))) == 3
    assert len(list(neighbors((1, 2, 3, 4, 0, 5, 6, 7, 8)))) == 4


def test_manhattan_ignores_the_blank():
    assert manhattan(goal_state(3)) == 0
    assert manhattan((1, 2, 3, 4, 5, 6, 7, 0, 8)) == 1
    assert manhattan((1, 2, 3, 4, 5, 0, 7, 8, 6)) == 1


def test_random_state_uses_each_value_once():
    assert sorted(random_state(3)) == list(range(9))
