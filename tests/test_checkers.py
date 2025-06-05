import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Damas - Controle por Clique")

class CheckersGame:
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        for y in range(3):
            for x in range(8):
                if (x + y) % 2 != 0:
                    self.board[y][x] = 2
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 != 0:
                    self.board[y][x] = 1
        self.selected = None
        self.running = True

    def draw_board(self):
        for y in range(8):
            for x in range(8):
                color = WHITE if (x + y) % 2 == 0 else BLACK
                pygame.draw.rect(window, color, (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if self.board[y][x] == 1:
                    pygame.draw.circle(window, RED, (x*SQUARE_SIZE + SQUARE_SIZE//2, y*SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE//2 - 10)
                elif self.board[y][x] == 2:
                    pygame.draw.circle(window, BLUE, (x*SQUARE_SIZE + SQUARE_SIZE//2, y*SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE//2 - 10)
        pygame.display.flip()

    def lidar_clique(self, pos):
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

    def run_game(self):
        while self.running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.lidar_clique(pygame.mouse.get_pos())
            self.draw_board()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jogo = CheckersGame()
    jogo.run_game()
