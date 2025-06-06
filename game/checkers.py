"""Módulo simplificado de jogo de damas controlado por voz."""

import pygame
import sys


pygame.init()

# ------------------------------
# Constantes de configuração
# ------------------------------
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8

# Cores utilizadas nas peças e tabuleiro
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Damas - Controle por Voz")

class CheckersGame:
    """Regras básicas de movimentação com interface em Pygame."""

    def __init__(self):
        """Cria o tabuleiro inicial e configura o estado do jogo."""
        self.board = self._create_board()
        self.selected = None
        self.running = True

    def _create_board(self):
        """Gera o tabuleiro na configuração inicial."""
        board = [[0 for _ in range(8)] for _ in range(8)]
        # Peças azuis nas três primeiras linhas
        for y in range(3):
            for x in range(8):
                if (x + y) % 2 != 0:
                    board[y][x] = 2
        # Peças vermelhas nas três últimas linhas
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 != 0:
                    board[y][x] = 1
        return board

    def draw_board(self):
        """Desenha tabuleiro e peças na janela."""
        for y in range(8):
            for x in range(8):
                color = WHITE if (x + y) % 2 == 0 else BLACK
                rect = (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(window, color, rect)
                if self.board[y][x] == 1:
                    pygame.draw.circle(
                        window,
                        RED,
                        (x * SQUARE_SIZE + SQUARE_SIZE // 2,
                         y * SQUARE_SIZE + SQUARE_SIZE // 2),
                        SQUARE_SIZE // 2 - 10,
                    )
                elif self.board[y][x] == 2:
                    pygame.draw.circle(
                        window,
                        BLUE,
                        (x * SQUARE_SIZE + SQUARE_SIZE // 2,
                         y * SQUARE_SIZE + SQUARE_SIZE // 2),
                        SQUARE_SIZE // 2 - 10,
                    )
        pygame.display.flip()

    def move_by_command(self, command):
        """Realiza um movimento interpretando uma string de comando."""
        words_to_numbers = {
            "um": 1, "dois": 2, "três": 3, "tres": 3, "quatro": 4,
            "cinco": 5, "seis": 6, "sete": 7, "oito": 8,
            "1": 1, "2": 2, "3": 3, "4": 4,
            "5": 5, "6": 6, "7": 7, "8": 8,
        }

        words = command.split()
        if (
            len(words) == 5
            and words[0] == "mover"
            and words[1] == "linha"
            and words[3] == "coluna"
        ):
            try:
                row = words_to_numbers.get(words[2].lower(), -1) - 1
                col = words_to_numbers.get(words[4].lower(), -1) - 1
                # Verifica se a posição é válida
                if 0 <= row < 8 and 0 <= col < 8:
                    piece = self.board[row][col]
                    if piece != 0:
                        new_row = row - 1 if piece == 1 else row + 1
                        if 0 <= new_row < 8 and self.board[new_row][col] == 0:
                            # Efetua a movimentação
                            self.board[new_row][col] = piece
                            self.board[row][col] = 0
                        else:
                            # Nova posição inválida ou ocupada
                            pass
                    else:
                        # Nenhuma peça na posição indicada
                        pass
                else:
                    # Posição fora do tabuleiro
                    pass
            except ValueError:
                # Falha ao interpretar números do comando
                pass
        else:
            # Estrutura do comando não reconhecida
            pass

    def run_game(self):
        """Executa o loop principal de desenho e eventos."""
        while self.running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False
            self.draw_board()

        pygame.quit()
        sys.exit()
