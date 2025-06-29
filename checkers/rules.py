"""Regras básicas de movimentação para o jogo de damas."""



from .board import (
    EMPTY,
    RED_PAWN,
    BLUE_PAWN,
    RED_KING,
    BLUE_KING,
    BOARD_SIZE,
)


def simple_moves(board: list[list[int]], x: int, y: int) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """Calcula movimentos simples (sem captura) para a peça em ``(x, y)``."""

    piece = board[y][x]
    moves: list[tuple[tuple[int, int], tuple[int, int]]] = []

    # Determina as direções possíveis conforme o tipo da peça
    if piece == RED_PAWN:  # Peça vermelha move para cima
        directions = [(-1, -1), (1, -1)]
    elif piece == BLUE_PAWN:  # Peça azul move para baixo
        directions = [(-1, 1), (1, 1)]
    elif piece in (RED_KING, BLUE_KING):  # Damas movem-se em todas as diagonais
        directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    else:
        return []  # Casa vazia ou valor inválido

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (
            0 <= nx < BOARD_SIZE
            and 0 <= ny < BOARD_SIZE
            and board[ny][nx] == EMPTY
        ):
            moves.append(((x, y), (nx, ny)))

    return moves


def capture_moves(board: list[list[int]], x: int, y: int) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """Calcula e retorna as capturas possíveis para a peça em ``(x, y)``."""

    piece = board[y][x]
    captures: list[tuple[tuple[int, int], tuple[int, int]]] = []

    if piece in (RED_PAWN, BLUE_PAWN):
        # Peças normais só capturam em uma direção vertical
        dir_y = -1 if piece == RED_PAWN else 1
        possibilities = [(-2, 2 * dir_y), (2, 2 * dir_y)]
        for dx, dy in possibilities:
            nx, ny = x + dx, y + dy
            mx, my = x + dx // 2, y + dy // 2
            if (
                0 <= nx < BOARD_SIZE
                and 0 <= ny < BOARD_SIZE
                and board[ny][nx] == EMPTY
                and board[my][mx] != EMPTY
                and (board[my][mx] % 2) != (piece % 2)
            ):
                captures.append(((x, y), (nx, ny)))

    elif piece in (RED_KING, BLUE_KING):
        # Damas capturam em qualquer diagonal
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            nx, ny = x + dx, y + dy
            mx, my = x + dx // 2, y + dy // 2
            if (
                0 <= nx < BOARD_SIZE
                and 0 <= ny < BOARD_SIZE
                and board[ny][nx] == EMPTY
                and board[my][mx] != EMPTY
                and (board[my][mx] % 2) != (piece % 2)
            ):
                captures.append(((x, y), (nx, ny)))

    return captures


def apply_move(board: list[list[int]], origin: tuple[int, int], destination: tuple[int, int]) -> bool:
    """Aplica um movimento e retorna ``True`` se for captura."""

    x0, y0 = origin
    x1, y1 = destination
    piece = board[y0][x0]

    # Verifica se o deslocamento corresponde a uma captura
    if abs(x1 - x0) == 2 and abs(y1 - y0) == 2:
        mx, my = (x0 + x1) // 2, (y0 + y1) // 2
        board[my][mx] = EMPTY  # remove peça capturada
        board[y1][x1] = piece
        board[y0][x0] = EMPTY
        return True

    # Movimento simples
    board[y1][x1] = piece
    board[y0][x0] = EMPTY
    return False


def promote_piece(board: list[list[int]], x: int, y: int) -> bool:
    """Promove a peça para dama caso alcance a borda do tabuleiro."""

    piece = board[y][x]

    if piece == RED_PAWN and y == 0:
        board[y][x] = RED_KING
        return True

    if piece == BLUE_PAWN and y == BOARD_SIZE - 1:
        board[y][x] = BLUE_KING
        return True

    return False

