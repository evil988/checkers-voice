# checkers/draw.py

import pygame

# Dimensões e cores
WIDTH, HEIGHT = 640, 640
MARGIN = 40
SQUARE_SIZE = (WIDTH - MARGIN) // 8
BOARD_WIDTH = SQUARE_SIZE * 8
BOARD_HEIGHT = SQUARE_SIZE * 8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

def draw_board(surface, board, highlighted_pos):
    """Draw the board to the given Pygame surface.

    Args:
        surface: pygame.Surface to draw on.
        board: 8x8 board state.
        highlighted_pos: optional (x, y) tuple to highlight.
    """
    fonte_label = pygame.font.SysFont(None, 24)
    surface.fill(BLACK)

    # Casas e peças
    for y in range(8):
        for x in range(8):
            # Cor da casa: branca (x+y par) ou preta (x+y ímpar)
            cor_casa = WHITE if (x + y) % 2 == 0 else BLACK
            rect = pygame.Rect(MARGIN + x * SQUARE_SIZE,
                               y * SQUARE_SIZE,
                               SQUARE_SIZE,
                               SQUARE_SIZE)
            pygame.draw.rect(surface, cor_casa, rect)

            # Destacar posição selecionada
            if highlighted_pos == (x, y):
                pygame.draw.rect(surface, GREEN, rect, 4)

            # Desenhar peça: 1 ou 3 = vermelha; 2 ou 4 = azul
            p = board[y][x]
            center = (MARGIN + x * SQUARE_SIZE + SQUARE_SIZE // 2,
                      y * SQUARE_SIZE + SQUARE_SIZE // 2)

            if p in (1, 3):
                pygame.draw.circle(surface, RED, center, SQUARE_SIZE // 2 - 10)
            if p in (2, 4):
                pygame.draw.circle(surface, BLUE, center, SQUARE_SIZE // 2 - 10)
            # Se dama (3 ou 4), coloca “D” em amarelo
            if p in (3, 4):
                d = pygame.font.SysFont(None, SQUARE_SIZE // 2).render('D', True, YELLOW)
                surface.blit(d, d.get_rect(center=center))

    # Rótulos de colunas (C1..C8) abaixo do tabuleiro
    col_labels = [f'C{i}' for i in range(1, 9)]
    for i, text in enumerate(col_labels):
        label = fonte_label.render(text, True, YELLOW)
        lx = MARGIN + i * SQUARE_SIZE + (SQUARE_SIZE - label.get_width()) // 2
        ly = BOARD_HEIGHT + (MARGIN - label.get_height()) // 2
        surface.blit(label, (lx, ly))

    # Rótulos de linhas (L1..L8) ao lado esquerdo
    row_labels = [f'L{j}' for j in range(1, 9)]
    for j, text in enumerate(row_labels):
        label = fonte_label.render(text, True, YELLOW)
        lx = (MARGIN - label.get_width()) // 2
        ly = j * SQUARE_SIZE + (SQUARE_SIZE - label.get_height()) // 2
        surface.blit(label, (lx, ly))

    pygame.display.flip()