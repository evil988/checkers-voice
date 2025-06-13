"""Pequeno utilitário Pygame para testar movimentação das peças por clique."""

import sys
import pygame


# ---------------------------------------------------------------------------
# Configurações do tabuleiro e cores
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)


def create_initial_board() -> list[list[int]]:
    """Gera a configuração inicial padrão de damas."""
    board = [[0 for _ in range(8)] for _ in range(8)]
    for y in range(3):
        for x in range(8):
            if (x + y) % 2 != 0:
                board[y][x] = 2
    for y in range(5, 8):
        for x in range(8):
            if (x + y) % 2 != 0:
                board[y][x] = 1
    return board


class CheckersGame:
    """Controla desenho e interação apenas via mouse."""

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.board = create_initial_board()
        self.selected: tuple[int, int] | None = None
        self.running = True

    def draw_board(self) -> None:
        """Desenha as casas e peças na superfície configurada."""
        for y in range(8):
            for x in range(8):
                color = WHITE if (x + y) % 2 == 0 else BLACK
                rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.surface, color, rect)

                piece = self.board[y][x]
                if piece == 1:
                    pygame.draw.circle(
                        self.surface,
                        RED,
                        (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2),
                        SQUARE_SIZE // 2 - 10,
                    )
                elif piece == 2:
                    pygame.draw.circle(
                        self.surface,
                        BLUE,
                        (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2),
                        SQUARE_SIZE // 2 - 10,
                    )
        pygame.display.flip()

    def lidar_clique(self, pos: tuple[int, int]) -> None:
        """Processa um clique do mouse em ``pos``."""
        x, y = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
        if self.selected:
            sel_x, sel_y = self.selected
            piece = self.board[sel_y][sel_x]
            if self.board[y][x] == 0:
                direction = -1 if piece == 1 else 1
                if y == sel_y + direction and abs(x - sel_x) == 1:
                    self.board[y][x] = piece
                    self.board[sel_y][sel_x] = 0
            self.selected = None
        else:
            if self.board[y][x] != 0:
                self.selected = (x, y)

    def run_game(self) -> None:
        """Loop principal da aplicação."""
        clock = pygame.time.Clock()
        while self.running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.lidar_clique(evento.pos)
            self.draw_board()
            clock.tick(30)

        pygame.quit()
        sys.exit()

def main() -> None:
    """Inicializa o Pygame e inicia a partida de teste."""
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Damas - Teste de Clique")
    CheckersGame(window).run_game()


if __name__ == "__main__":
    main()
