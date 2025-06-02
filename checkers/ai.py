# checkers/ai.py

import random
from .rules import movimentos_simples, movimentos_captura

def escolher_jogada_aleatoria(tabuleiro):
    """
    Para o jogador 'azul' (peça 2 ou dama 4), coleta todos os movimentos possíveis
    (simples + captura) e escolhe aleatoriamente um.
    Retorna (origem, destino, houve_captura).
    """
    movs = []
    coroas = [2, 4]  # 2=peça normal azul; 4=dama azul

    for y in range(8):
        for x in range(8):
            if tabuleiro[y][x] in coroas:
                # Capturas têm prioridade
                caps = movimentos_captura(tabuleiro, x, y)
                if caps:
                    for m in caps:
                        movs.append((m, True))
                else:
                    sims = movimentos_simples(tabuleiro, x, y)
                    for m in sims:
                        movs.append((m, False))

    if not movs:
        return None  # sem jogadas possíveis (fim de jogo)

    (origem, destino), captura = random.choice(movs)
    return origem, destino, captura
