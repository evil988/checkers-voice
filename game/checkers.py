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
pygame.display.set_caption("Damas - Controle por Voz")

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

    def move_by_command(self, command):
        words_to_numbers = {
            "um": 1, "dois": 2, "três": 3, "tres": 3, "quatro": 4,
            "cinco": 5, "seis": 6, "sete": 7, "oito": 8,
            "1": 1, "2": 2, "3": 3, "4": 4,
            "5": 5, "6": 6, "7": 7, "8": 8
        }
        print(f"Recebido comando: {command}")
        words = command.split()
        if len(words) == 5 and words[0] in ['mover'] and words[1] == 'linha' and words[3] == 'coluna':
            print("Formato do comando reconhecido corretamente")
            try:
                row = words_to_numbers.get(words[2].lower(), -1) - 1
                col = words_to_numbers.get(words[4].lower(), -1) - 1
                print(f"Posição interpretada: linha={row}, coluna={col}")
                if 0 <= row < 8 and 0 <= col < 8:
                    piece = self.board[row][col]
                    print(f"Valor da peça na posição: {piece}")
                    if piece != 0:
                        new_row = row - 1 if piece == 1 else row + 1
                        print(f"Tentando mover para linha {new_row}, coluna {col}")
                        if 0 <= new_row < 8 and self.board[new_row][col] == 0:
                            self.board[new_row][col] = piece
                            self.board[row][col] = 0
                            print("Movimento realizado com sucesso")
                        else:
                            print("Nova posição inválida ou ocupada")
                    else:
                        print("posição sem peça")
                else:
                    print("Posição fora dos limites do tabuleiro")
            except ValueError:
                print("Erro ao converter linha ou coluna para inteiro")
        else:
            print("Comando inválido ou mal formatado")

    def run_game(self):
        while self.running:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.running = False
            self.draw_board()

        pygame.quit()
        sys.exit()
