# checkers/draw.py

import pygame

# Dimensões e cores
LARGURA, ALTURA = 640, 640
MARGIN = 40
TAMANHO_CASA = (LARGURA - MARGIN) // 8
BOARD_WIDTH = TAMANHO_CASA * 8
BOARD_HEIGHT = TAMANHO_CASA * 8

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

def draw_board(surface, board, highlighted_pos):
    """Draw the board to the given Pygame surface.

    Args:
        surface: pygame.Surface to draw on.
        board: 8x8 board state.
        highlighted_pos: optional (x, y) tuple to highlight.
    """
    fonte_label = pygame.font.SysFont(None, 24)
    surface.fill(PRETO)

    # Casas e peças
    for y in range(8):
        for x in range(8):
            # Cor da casa: branca (x+y par) ou preta (x+y ímpar)
            cor_casa = BRANCO if (x + y) % 2 == 0 else PRETO
            rect = pygame.Rect(MARGIN + x * TAMANHO_CASA,
                               y * TAMANHO_CASA,
                               TAMANHO_CASA,
                               TAMANHO_CASA)
            pygame.draw.rect(surface, cor_casa, rect)

            # Destacar posição selecionada
            if highlighted_pos == (x, y):
                pygame.draw.rect(surface, VERDE, rect, 4)

            # Desenhar peça: 1 ou 3 = vermelha; 2 ou 4 = azul
            p = board[y][x]
            center = (MARGIN + x * TAMANHO_CASA + TAMANHO_CASA // 2,
                      y * TAMANHO_CASA + TAMANHO_CASA // 2)

            if p in (1, 3):
                pygame.draw.circle(surface, VERMELHO, center, TAMANHO_CASA // 2 - 10)
            if p in (2, 4):
                pygame.draw.circle(surface, AZUL, center, TAMANHO_CASA // 2 - 10)
            # Se dama (3 ou 4), coloca “D” em amarelo
            if p in (3, 4):
                d = pygame.font.SysFont(None, TAMANHO_CASA // 2).render('D', True, AMARELO)
                surface.blit(d, d.get_rect(center=center))

    # Rótulos de colunas (C1..C8) abaixo do tabuleiro
    col_labels = [f'C{i}' for i in range(1, 9)]
    for i, text in enumerate(col_labels):
        label = fonte_label.render(text, True, AMARELO)
        lx = MARGIN + i * TAMANHO_CASA + (TAMANHO_CASA - label.get_width()) // 2
        ly = BOARD_HEIGHT + (MARGIN - label.get_height()) // 2
        surface.blit(label, (lx, ly))

    # Rótulos de linhas (L1..L8) ao lado esquerdo
    row_labels = [f'L{j}' for j in range(1, 9)]
    for j, text in enumerate(row_labels):
        label = fonte_label.render(text, True, AMARELO)
        lx = (MARGIN - label.get_width()) // 2
        ly = j * TAMANHO_CASA + (TAMANHO_CASA - label.get_height()) // 2
        surface.blit(label, (lx, ly))

    pygame.display.flip()
