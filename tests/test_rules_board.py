from checkers.board import (
    Board,
    EMPTY,
    RED_PAWN,
    BLUE_PAWN,
    RED_KING,
    BLUE_KING,
    BOARD_SIZE,
    INITIAL_ROWS,
)
from checkers import rules


def test_board_initialization_counts():
    board = Board()
    reds = sum(row.count(RED_PAWN) for row in board.grid)
    blues = sum(row.count(BLUE_PAWN) for row in board.grid)
    assert reds == INITIAL_ROWS * 4
    assert blues == INITIAL_ROWS * 4


def test_simple_moves():
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[5][2] = RED_PAWN
    board[2][4] = BLUE_PAWN
    board[3][3] = RED_KING
    moves_red = rules.simple_moves(board, 2, 5)
    moves_blue = rules.simple_moves(board, 4, 2)
    moves_king = rules.simple_moves(board, 3, 3)
    assert set(moves_red) == {((2, 5), (1, 4)), ((2, 5), (3, 4))}
    assert set(moves_blue) == {((4, 2), (5, 3))}
    assert set(moves_king) == {
        ((3, 3), (2, 2)),
        ((3, 3), (2, 4)),
        ((3, 3), (4, 4)),
    }


def test_capture_moves():
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[5][2] = RED_PAWN
    board[4][3] = BLUE_PAWN
    board[2][4] = BLUE_PAWN
    board[3][3] = RED_KING
    captures_red = rules.capture_moves(board, 2, 5)
    captures_king = rules.capture_moves(board, 3, 3)
    assert captures_red == [((2, 5), (4, 3))]
    assert set(captures_king) == {((3, 3), (5, 1))}


def test_promote_piece():
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    board[0][1] = RED_PAWN
    board[BOARD_SIZE - 1][2] = BLUE_PAWN
    assert rules.promote_piece(board, 1, 0) is True
    assert board[0][1] == RED_KING
    assert rules.promote_piece(board, 2, BOARD_SIZE - 1) is True
    assert board[BOARD_SIZE - 1][2] == BLUE_KING
    # No promotion when not at final row
    board[3][3] = RED_PAWN
    assert rules.promote_piece(board, 3, 3) is False