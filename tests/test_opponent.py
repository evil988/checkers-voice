import pytest

from checkers.board import EMPTY, BLUE_PAWN, RED_PAWN, BOARD_SIZE
from checkers.opponent import choose_random_move
from checkers import rules


def test_choose_random_move_returns_capture():
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[2][2] = BLUE_PAWN
    board[3][1] = RED_PAWN
    board[3][3] = RED_PAWN

    origin, dest, captured = choose_random_move(board)
    assert captured is True
    assert (origin, dest) in rules.capture_moves(board, 2, 2)