# checkers/ai.py

import random
from .rules import simple_moves, capture_moves

def choose_random_move(board):
    """
    Para o jogador 'azul' (peça 2 ou dama 4), coleta todos os movimentos possíveis
    (simples + captura) e escolhe aleatoriamente um.
    Retorna (origem, destino, houve_captura).
    """
    moves = []
    crowns = [2, 4]  # 2=peça normal azul; 4=dama azul

    for y in range(8):
        for x in range(8):
            if board[y][x] in crowns:
                # Capturas têm prioridade
                caps = capture_moves(board, x, y)
                if caps:
                    for m in caps:
                        moves.append((m, True))
                else:
                    sims = simple_moves(board, x, y)
                    for m in sims:
                        moves.append((m, False))

    if not moves:
        return None  # sem jogadas possíveis (fim de jogo)

    (origin, dest), capture = random.choice(moves)
    return origin, dest, capture
