# checkers/opponent.py
"""Funções relacionadas aos movimentos do adversário controlado pelo computador."""

import random
from typing import Optional

from .board import BLUE_PAWN, BLUE_KING, BOARD_SIZE
from .rules import simple_moves, capture_moves


def choose_random_move(board: list[list[int]]) -> Optional[tuple[tuple[int, int], tuple[int, int], bool]]:
    """Seleciona um movimento aleatório para o jogador azul.

    Percorre todas as peças azuis (``BLUE_PAWN`` e ``BLUE_KING``) em busca de
    movimentos possíveis. Capturas sempre têm prioridade sobre movimentos
    simples. Caso nenhum movimento esteja disponível, ``None`` é retornado.

    Retorna uma tupla ``(origem, destino, houve_captura)``.
    """

    moves: list[tuple[tuple[tuple[int, int], tuple[int, int]], bool]] = []
    blue_pieces = [BLUE_PAWN, BLUE_KING]

    # Percorre o tabuleiro em busca de peças azuis
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] in blue_pieces:
                # Primeiro verifica se há capturas disponíveis
                captures = capture_moves(board, x, y)
                if captures:
                    for move in captures:
                        # Marca cada jogada como captura (True)
                        moves.append((move, True))
                else:
                    # Sem capturas: coleta movimentos simples
                    simples = simple_moves(board, x, y)
                    for move in simples:
                        moves.append((move, False))

    if not moves:
        # Nenhuma jogada disponível: provavelmente fim de jogo
        return None

    # Escolhe aleatoriamente um movimento coletado
    (origin, dest), capture = random.choice(moves)
    return origin, dest, capture