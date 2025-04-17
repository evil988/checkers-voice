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
pygame.display.set_caption("Damas - Controle por Voz")

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

    def mover_por_comando(self, comando):
        palavras_para_numeros = {
            "um": 1, "dois": 2, "três": 3, "tres": 3, "quatro": 4,
            "cinco": 5, "seis": 6, "sete": 7, "oito": 8,
            "1": 1, "2": 2, "3": 3, "4": 4,
            "5": 5, "6": 6, "7": 7, "8": 8
        }
        print(f"Recebido comando: {comando}")
        palavras = comando.split()
        if len(palavras) == 5 and palavras[0] in ['mover'] and palavras[1] == 'linha' and palavras[3] == 'coluna':
            print("Formato do comando reconhecido corretamente")
            try:
                linha = palavras_para_numeros.get(palavras[2].lower(), -1) - 1
                coluna = palavras_para_numeros.get(palavras[4].lower(), -1) - 1
                print(f"Posição interpretada: linha={linha}, coluna={coluna}")
                if 0 <= linha < 8 and 0 <= coluna < 8:
                    peca = self.tabuleiro[linha][coluna]
                    print(f"Valor da peça na posição: {peca}")
                    if peca != 0:
                        nova_linha = linha - 1 if peca == 1 else linha + 1
                        print(f"Tentando mover para linha {nova_linha}, coluna {coluna}")
                        if 0 <= nova_linha < 8 and self.tabuleiro[nova_linha][coluna] == 0:
                            self.tabuleiro[nova_linha][coluna] = peca
                            self.tabuleiro[linha][coluna] = 0
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

    def rodar_jogo(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
            self.desenhar_tabuleiro()

        pygame.quit()
        sys.exit()
