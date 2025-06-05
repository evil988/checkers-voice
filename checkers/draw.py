"""Funções utilitárias para desenhar o tabuleiro de damas."""

import pygame

# Dimensões do tabuleiro e cores utilizadas
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
    # Fonte padrão utilizada para rótulos
    label_font = pygame.font.SysFont(None, 24)

    # Preenche a superfície com a cor de fundo
    surface.fill(BLACK)

    # Casas e peças
    for y in range(8):
        for x in range(8):
            # Cor do quadrado: branca quando (x+y) é par, preta caso contrário
            square_color = WHITE if (x + y) % 2 == 0 else BLACK
            rect = pygame.Rect(MARGIN + x * SQUARE_SIZE,
                               y * SQUARE_SIZE,
                               SQUARE_SIZE,
                               SQUARE_SIZE)
            pygame.draw.rect(surface, square_color, rect)

            # Destacar posição selecionada
            if highlighted_pos == (x, y):
                pygame.draw.rect(surface, GREEN, rect, 4)

            # Desenhar peça: 1 ou 3 = vermelha; 2 ou 4 = azul
            piece = board[y][x]
            center = (MARGIN + x * SQUARE_SIZE + SQUARE_SIZE // 2,
                      y * SQUARE_SIZE + SQUARE_SIZE // 2)

            # Desenha círculos vermelhos ou azuis conforme o valor da peça
            if piece in (1, 3):
                pygame.draw.circle(surface, RED, center, SQUARE_SIZE // 2 - 10)
            if piece in (2, 4):
                pygame.draw.circle(surface, BLUE, center, SQUARE_SIZE // 2 - 10)

            # Para damas (3 ou 4) adiciona o rótulo "D" em amarelo
            if piece in (3, 4):
                king_label = pygame.font.SysFont(None, SQUARE_SIZE // 2).render('D', True, YELLOW)
                surface.blit(king_label, king_label.get_rect(center=center))

    # Rótulos de colunas (C1..C8) posicionados abaixo do tabuleiro
    col_labels = [f'C{i}' for i in range(1, 9)]
    for i, text in enumerate(col_labels):
        label = label_font.render(text, True, YELLOW)
        lx = MARGIN + i * SQUARE_SIZE + (SQUARE_SIZE - label.get_width()) // 2
        ly = BOARD_HEIGHT + (MARGIN - label.get_height()) // 2
        surface.blit(label, (lx, ly))

    # Rótulos de linhas (L1..L8) exibidos na lateral esquerda
    row_labels = [f'L{j}' for j in range(1, 9)]
    for j, text in enumerate(row_labels):
        label = label_font.render(text, True, YELLOW)
        lx = (MARGIN - label.get_width()) // 2
        ly = j * SQUARE_SIZE + (SQUARE_SIZE - label.get_height()) // 2
        surface.blit(label, (lx, ly))

    pygame.display.flip()