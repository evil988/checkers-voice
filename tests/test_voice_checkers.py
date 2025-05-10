import pygame
import sys
import os
import json
import random
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

    comandos_menu = json.dumps(["um jogador", "dois jogadores", "sair"])
    model_path = os.path.join("assets", "model")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000, comandos_menu)
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000,
                        input=True, frames_per_buffer=8192)
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
                stream.stop_stream()
                stream.close()
                audio.terminate()

                if text == "um jogador":
                    return 1
                elif text == "dois jogadores":
                    return 2
                elif text == "sair":
                    pygame.quit()
                    sys.exit()


class VoiceControlledCheckers:
    def __init__(self, mode):
        self.mode = mode  # 1 = um jogador, 2 = dois jogadores
        self.inicializar_tabuleiro()
        self.rodando = True
        self.selecionado = None
        self.posicao_destacada = None

        self.numeros = ['um', 'dois', 'tres', 'quatro',
                        'cinco', 'seis', 'sete', 'oito']
        frases_validas = [f"linha {l} coluna {c}"
                          for l in self.numeros for c in self.numeros] + [
                          "cancelar", "reiniciar", "voltar ao menu principal"]
        grammar = json.dumps(frases_validas)

        model_path = os.path.join("assets", "model")
        if not os.path.exists(model_path):
            print("Modelo Vosk não encontrado. Coloque-o em 'assets/model'")
            sys.exit(1)

        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000, grammar)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1, rate=16000,
                                      input=True, frames_per_buffer=8192)
        self.stream.start_stream()

    def inicializar_tabuleiro(self):
        self.tabuleiro = [[0 for _ in range(8)] for _ in range(8)]
        for y in range(3):
            for x in range(8):
                if (x + y) % 2 != 0:
                    self.tabuleiro[y][x] = 2  # azuis
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 != 0:
                    self.tabuleiro[y][x] = 1  # vermelhas

    def desenhar_tabuleiro(self):
        for y in range(8):
            for x in range(8):
                cor = BRANCO if (x + y) % 2 == 0 else PRETO
                pygame.draw.rect(janela, cor,
                                 (x * TAMANHO_CASA,
                                  y * TAMANHO_CASA,
                                  TAMANHO_CASA, TAMANHO_CASA))

                if self.posicao_destacada == (x, y):
                    pygame.draw.rect(janela, VERDE,
                                     (x * TAMANHO_CASA,
                                      y * TAMANHO_CASA,
                                      TAMANHO_CASA, TAMANHO_CASA), 4)

                if self.tabuleiro[y][x] == 1:
                    pygame.draw.circle(janela, VERMELHO,
                                       (x * TAMANHO_CASA + TAMANHO_CASA // 2,
                                        y * TAMANHO_CASA + TAMANHO_CASA // 2),
                                       TAMANHO_CASA // 2 - 10)
                elif self.tabuleiro[y][x] == 2:
                    pygame.draw.circle(janela, AZUL,
                                       (x * TAMANHO_CASA + TAMANHO_CASA // 2,
                                        y * TAMANHO_CASA + TAMANHO_CASA // 2),
                                       TAMANHO_CASA // 2 - 10)
        pygame.display.flip()

    def escutar_comando(self):
        data = self.stream.read(8192, exception_on_overflow=False)
        if self.recognizer.AcceptWaveform(data):
            result = json.loads(self.recognizer.Result())
            text = result.get("text", "").strip()
            if text:
                if text == "cancelar":
                    return "cancelar"
                if text == "reiniciar":
                    return "reiniciar"
                if text == "voltar ao menu principal":
                    return "menu"
                palavras = text.split()
                if len(palavras) == 4 and palavras[0] == "linha" and palavras[2] == "coluna":
                    if palavras[1] in self.numeros and palavras[3] in self.numeros:
                        return (palavras[1], palavras[3])
        return None

    def executar_jogada_azul(self):
        movimentos = []
        # coleta movimentos simples e de captura das peças azuis (2)
        for y in range(8):
            for x in range(8):
                if self.tabuleiro[y][x] == 2:
                    # direção de movimento das azuis: +1 (para baixo)
                    for dx in (-1, 1):
                        nx, ny = x + dx, y + 1
                        if 0 <= nx < 8 and 0 <= ny < 8 and self.tabuleiro[ny][nx] == 0:
                            movimentos.append(((x, y), (nx, ny)))
                    # capturas
                    for dx in (-2, 2):
                        nx, ny = x + dx, y + 2
                        mid_x, mid_y = x + dx // 2, y + 1
                        if (0 <= nx < 8 and 0 <= ny < 8 and
                                self.tabuleiro[ny][nx] == 0 and
                                self.tabuleiro[mid_y][mid_x] == 1):
                            movimentos.append(((x, y), (nx, ny)))
        if movimentos:
            origem, destino = random.choice(movimentos)
            x0, y0 = origem
            x1, y1 = destino
            # se for captura
            if abs(x1 - x0) == 2:
                mid_x, mid_y = (x0 + x1) // 2, (y0 + y1) // 2
                self.tabuleiro[mid_y][mid_x] = 0
            self.tabuleiro[y1][x1] = 2
            self.tabuleiro[y0][x0] = 0
            print(f"🤖 Azul moveu de {origem} para {destino}")
        else:
            print("🤖 Azul sem jogadas possíveis")

    def iniciar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False

            comando = self.escutar_comando()
            if comando:
                if comando == "cancelar":
                    if self.posicao_destacada is not None:
                        self.posicao_destacada = None
                        print("✅ Destaque removido")
                elif comando == "reiniciar":
                    self.inicializar_tabuleiro()
                    self.posicao_destacada = None
                    print("🔄 Jogo reiniciado")
                elif comando == "menu":
                    print("🔙 Retornando ao menu principal")
                    return "menu"
                else:
                    linha_str, coluna_str = comando
                    linha_idx = self.numeros.index(linha_str)
                    coluna_idx = self.numeros.index(coluna_str)

                    if self.posicao_destacada is None:
                        peca = self.tabuleiro[linha_idx][coluna_idx]
                        if peca == 0:
                            print("❌ Não há peça nessa posição")
                        elif self.mode == 1 and peca != 1:
                            print("❌ Modo 1 jogador: só peças vermelhas podem ser selecionadas")
                        else:
                            self.posicao_destacada = (coluna_idx, linha_idx)
                            print(f"🟩 Posição {self.posicao_destacada} destacada")
                    else:
                        origem = self.posicao_destacada
                        destino = (coluna_idx, linha_idx)
                        peca = self.tabuleiro[origem[1]][origem[0]]

                        # Jogada simples
                        if (self.tabuleiro[destino[1]][destino[0]] == 0 and
                            destino[1] == origem[1] + (-1 if peca == 1 else 1) and
                            abs(destino[0] - origem[0]) == 1):
                            self.tabuleiro[destino[1]][destino[0]] = peca
                            self.tabuleiro[origem[1]][origem[0]] = 0
                            print(f"✅ Peça movida de {origem} para {destino}")
                            if self.mode == 1:
                                self.executar_jogada_azul()

                        # Captura
                        elif (self.tabuleiro[destino[1]][destino[0]] == 0 and
                              destino[1] == origem[1] + 2 * (-1 if peca == 1 else 1) and
                              abs(destino[0] - origem[0]) == 2):
                            meio_x = (origem[0] + destino[0]) // 2
                            meio_y = (origem[1] + destino[1]) // 2
                            peca_meio = self.tabuleiro[meio_y][meio_x]
                            if peca_meio != 0 and peca_meio != peca:
                                self.tabuleiro[destino[1]][destino[0]] = peca
                                self.tabuleiro[origem[1]][origem[0]] = 0
                                self.tabuleiro[meio_y][meio_x] = 0
                                print(f"🗑️ Captura de {origem} para {destino}")
                                if self.mode == 1:
                                    self.executar_jogada_azul()
                            else:
                                print("❌ Captura inválida")
                        else:
                            print("❌ Movimento inválido")

                        self.posicao_destacada = None

            self.desenhar_tabuleiro()

        # Limpeza ao sair
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    while True:
        modo = mostrar_menu()
        if modo in (1, 2):
            app = VoiceControlledCheckers(modo)
            resultado = app.iniciar()
            if resultado == "menu":
                continue
            else:
                break
        else:
            break
