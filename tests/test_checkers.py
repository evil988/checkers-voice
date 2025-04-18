import pygame
import sys

pygame.init()

LARGURA, ALTURA = 640, 640
TAMANHO_CASA = LARGURA // 8

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 255)

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Damas - Controle por Clique")

class CheckersGame:
    def __init__(self):
        self.tabuleiro = [[0 for _ in range(8)] for _ in range(8)]
        for y in range(3):
            for x in range(8):
                if (x + y) % 2 != 0:
                    self.tabuleiro[y][x] = 2
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 != 0:
                    self.tabuleiro[y][x] = 1
        self.selecionado = None
        self.rodando = True

    def desenhar_tabuleiro(self):
        for y in range(8):
            for x in range(8):
                cor = BRANCO if (x + y) % 2 == 0 else PRETO
                pygame.draw.rect(janela, cor, (x*TAMANHO_CASA, y*TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA))
                if self.tabuleiro[y][x] == 1:
                    pygame.draw.circle(janela, VERMELHO, (x*TAMANHO_CASA + TAMANHO_CASA//2, y*TAMANHO_CASA + TAMANHO_CASA//2), TAMANHO_CASA//2 - 10)
                elif self.tabuleiro[y][x] == 2:
                    pygame.draw.circle(janela, AZUL, (x*TAMANHO_CASA + TAMANHO_CASA//2, y*TAMANHO_CASA + TAMANHO_CASA//2), TAMANHO_CASA//2 - 10)
        pygame.display.flip()

    def lidar_clique(self, pos):
        x, y = pos[0] // TAMANHO_CASA, pos[1] // TAMANHO_CASA
        if self.selecionado:
            sel_x, sel_y = self.selecionado
            peca = self.tabuleiro[sel_y][sel_x]
            if self.tabuleiro[y][x] == 0:
                direcao = -1 if peca == 1 else 1
                if y == sel_y + direcao and abs(x - sel_x) == 1:
                    self.tabuleiro[y][x] = peca
                    self.tabuleiro[sel_y][sel_x] = 0
            self.selecionado = None
        else:
            if self.tabuleiro[y][x] != 0:
                self.selecionado = (x, y)

    def rodar_jogo(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self.lidar_clique(pygame.mouse.get_pos())
            self.desenhar_tabuleiro()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jogo = CheckersGame()
    jogo.rodar_jogo()
