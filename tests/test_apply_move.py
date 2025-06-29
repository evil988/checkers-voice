import pytest

from checkers.board import (
    EMPTY,
    RED_PAWN,
    BLUE_PAWN,
    BOARD_SIZE,
)
from checkers import rules


def test_apply_move_simple():
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[5][2] = RED_PAWN

    result = rules.apply_move(board, (2, 5), (3, 4))

    assert result is False
    assert board[5][2] == EMPTY
    assert board[4][3] == RED_PAWN


def test_apply_move_capture():
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[5][2] = RED_PAWN
    board[4][3] = BLUE_PAWN

    result = rules.apply_move(board, (2, 5), (4, 3))

    assert result is True
    assert board[5][2] == EMPTY
    assert board[4][3] == EMPTY
    assert board[3][4] == RED_PAWN