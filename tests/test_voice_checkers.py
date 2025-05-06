import pygame
import sys
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# Inicialização do Pygame
pygame.init()
LARGURA, ALTURA = 640, 640
TAMANHO_CASA = LARGURA // 8

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Damas - Controle por Voz")

def mostrar_menu():
    fonte = pygame.font.SysFont(None, 60)
    janela.fill(PRETO)

    opcao1 = fonte.render("1 Jogador", True, BRANCO)
    opcao2 = fonte.render("2 Jogadores", True, BRANCO)
    opcao3 = fonte.render("Sair", True, BRANCO)

    rect1 = opcao1.get_rect(center=(LARGURA // 2, ALTURA // 2 - 60))
    rect2 = opcao2.get_rect(center=(LARGURA // 2, ALTURA // 2))
    rect3 = opcao3.get_rect(center=(LARGURA // 2, ALTURA // 2 + 60))

    janela.blit(opcao1, rect1)
    janela.blit(opcao2, rect2)
    janela.blit(opcao3, rect3)
    pygame.display.flip()

    # Reconhecimento de voz para selecionar o modo
    comandos_menu = json.dumps(["um jogador", "dois jogadores", "sair"])
    model_path = os.path.join("assets", "model")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000, comandos_menu)
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        data = stream.read(8192, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip()
            if text:
                print("\U0001F3A7 Comando no menu:", text)
                if text == "um jogador":
                    print("Modo 1 jogador selecionado (ainda não implementado)")
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    return 1
                elif text == "dois jogadores":
                    print("Modo 2 jogadores selecionado")
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    return 2
                elif text == "sair":
                    print("Encerrando o programa por comando de voz")
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    pygame.quit()
                    sys.exit()

class VoiceControlledCheckers:
    def __init__(self):
        self.inicializar_tabuleiro()
        self.rodando = True
        self.selecionado = None
        self.posicao_destacada = None

        self.numeros = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito']
        frases_validas = [f"linha {l} coluna {c}" for l in self.numeros for c in self.numeros] + ["cancelar", "reiniciar", "voltar ao menu principal"]
        grammar = json.dumps(frases_validas)

        model_path = os.path.join("assets", "model")
        if not os.path.exists(model_path):
            print("Modelo Vosk não encontrado. Coloque-o em 'assets/model'")
            sys.exit(1)

        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000, grammar)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()

    def inicializar_tabuleiro(self):
        self.tabuleiro = [[0 for _ in range(8)] for _ in range(8)]
        for y in range(3):
            for x in range(8):
                if (x + y) % 2 != 0:
                    self.tabuleiro[y][x] = 2
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 != 0:
                    self.tabuleiro[y][x] = 1

    def desenhar_tabuleiro(self):
        for y in range(8):
            for x in range(8):
                cor = BRANCO if (x + y) % 2 == 0 else PRETO
                pygame.draw.rect(janela, cor, (x*TAMANHO_CASA, y*TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA))

                if self.posicao_destacada == (x, y):
                    pygame.draw.rect(janela, VERDE, (x*TAMANHO_CASA, y*TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA), 4)

                if self.tabuleiro[y][x] == 1:
                    pygame.draw.circle(janela, VERMELHO, (x*TAMANHO_CASA + TAMANHO_CASA//2, y*TAMANHO_CASA + TAMANHO_CASA//2), TAMANHO_CASA//2 - 10)
                elif self.tabuleiro[y][x] == 2:
                    pygame.draw.circle(janela, AZUL, (x*TAMANHO_CASA + TAMANHO_CASA//2, y*TAMANHO_CASA + TAMANHO_CASA//2), TAMANHO_CASA//2 - 10)
        pygame.display.flip()

    def escutar_comando(self):
        data = self.stream.read(8192, exception_on_overflow=False)
        if self.recognizer.AcceptWaveform(data):
            result = json.loads(self.recognizer.Result())
            text = result.get("text", "").strip()
            if text:
                print("\U0001F3A7 Frase capturada:", text)
                if text == "cancelar":
                    print("\u274C Comando de cancelamento reconhecido")
                    return "cancelar"
                if text == "reiniciar":
                    print("\U0001F501 Comando de reinício reconhecido")
                    return "reiniciar"
                if text == "voltar ao menu principal":
                    print("\U0001F519 Retornando ao menu principal")
                    return "menu"
                palavras = text.split()
                if len(palavras) != 4:
                    print("\u26A0\uFE0F Frase ignorada (formato inválido, esperado 4 palavras):", palavras)
                    return None
                if palavras[0] != "linha" or palavras[2] != "coluna":
                    print("\u26A0\uFE0F Frase ignorada (estrutura esperada: 'linha X coluna Y')")
                    return None
                if palavras[1] not in self.numeros or palavras[3] not in self.numeros:
                    print("\u26A0\uFE0F Frase ignorada (números não reconhecidos):", palavras[1], palavras[3])
                    return None
                print("\u2705 Frase válida detectada")
                return palavras[1], palavras[3]
        return None

    def iniciar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False

            comando = self.escutar_comando()
            if comando:
                print("\U0001F3A4 Comando recebido:", comando)
                if comando == "cancelar":
                    if self.posicao_destacada is not None:
                        print("\u2705 Destaque removido")
                        self.posicao_destacada = None
                    else:
                        print("\u2139\uFE0F Nenhuma posição estava destacada")
                elif comando == "reiniciar":
                    self.inicializar_tabuleiro()
                    self.posicao_destacada = None
                    print("\U0001F501 Jogo reiniciado para posição inicial")
                elif comando == "menu":
                    print("\U0001F519 Encerrando partida e retornando ao menu principal")
                    return "menu"
                else:
                    linha_str, coluna_str = comando
                    linha_idx = self.numeros.index(linha_str)
                    coluna_idx = self.numeros.index(coluna_str)
                    if self.posicao_destacada is None:
                        self.posicao_destacada = (coluna_idx, linha_idx)
                        print(f"\U0001F7E9 Posição {self.posicao_destacada} destacada")
                    else:
                        origem = self.posicao_destacada
                        destino = (coluna_idx, linha_idx)
                        peca = self.tabuleiro[origem[1]][origem[0]]
                        if self.tabuleiro[destino[1]][destino[0]] == 0:
                            direcao = -1 if peca == 1 else 1
                            if destino[1] == origem[1] + direcao and abs(destino[0] - origem[0]) == 1:
                                self.tabuleiro[destino[1]][destino[0]] = peca
                                self.tabuleiro[origem[1]][origem[0]] = 0
                                print(f"\u2705 Peça movida de {origem} para {destino}")
                            elif destino[1] == origem[1] + 2 * direcao and abs(destino[0] - origem[0]) == 2:
                                meio_x = (origem[0] + destino[0]) // 2
                                meio_y = (origem[1] + destino[1]) // 2
                                peca_meio = self.tabuleiro[meio_y][meio_x]
                                if peca_meio != 0 and peca_meio != peca:
                                    self.tabuleiro[destino[1]][destino[0]] = peca
                                    self.tabuleiro[origem[1]][origem[0]] = 0
                                    self.tabuleiro[meio_y][meio_x] = 0
                                    print(f"\U0001F5D1️ Captura realizada de {origem} para {destino} eliminando ({meio_x}, {meio_y})")
                                else:
                                    print("\u274C Movimento de captura inválido")
                            else:
                                print("\u274C Movimento inválido")
                        else:
                            print("\u274C Destino ocupado")
                        self.posicao_destacada = None

            self.desenhar_tabuleiro()

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    while True:
        modo = mostrar_menu()
        if modo == 2:
            app = VoiceControlledCheckers()
            resultado = app.iniciar()
            if resultado == "menu":
                continue
            else:
                break
        else:
            break
