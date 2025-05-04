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

class VoiceControlledCheckers:
    def __init__(self):
        self.inicializar_tabuleiro()
        self.rodando = True
        self.selecionado = None
        self.posicao_destacada = None

        self.numeros = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito']
        frases_validas = [f"linha {l} coluna {c}" for l in self.numeros for c in self.numeros] + ["cancelar", "reiniciar"]
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
                print("🎧 Frase capturada:", text)
                if text == "cancelar":
                    print("🚫 Comando de cancelamento reconhecido")
                    return "cancelar"
                if text == "reiniciar":
                    print("🔄 Comando de reinício reconhecido")
                    return "reiniciar"
                palavras = text.split()
                if len(palavras) != 4:
                    print("⚠️ Frase ignorada (formato inválido, esperado 4 palavras):", palavras)
                    return None
                if palavras[0] != "linha" or palavras[2] != "coluna":
                    print("⚠️ Frase ignorada (estrutura esperada: 'linha X coluna Y')")
                    return None
                if palavras[1] not in self.numeros or palavras[3] not in self.numeros:
                    print("⚠️ Frase ignorada (números não reconhecidos):", palavras[1], palavras[3])
                    return None
                print("✅ Frase válida detectada")
                return palavras[1], palavras[3]
        return None

    def iniciar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False

            comando = self.escutar_comando()
            if comando:
                print("🎤 Comando recebido:", comando)
                if comando == "cancelar":
                    if self.posicao_destacada is not None:
                        print("✅ Destaque removido")
                        self.posicao_destacada = None
                    else:
                        print("ℹ️ Nenhuma posição estava destacada")
                elif comando == "reiniciar":
                    self.inicializar_tabuleiro()
                    self.posicao_destacada = None
                    print("🔁 Jogo reiniciado para posição inicial")
                else:
                    linha_str, coluna_str = comando
                    linha_idx = self.numeros.index(linha_str)
                    coluna_idx = self.numeros.index(coluna_str)
                    if self.posicao_destacada is None:
                        self.posicao_destacada = (coluna_idx, linha_idx)
                        print(f"🟩 Posição {self.posicao_destacada} destacada")
                    else:
                        origem = self.posicao_destacada
                        destino = (coluna_idx, linha_idx)
                        peca = self.tabuleiro[origem[1]][origem[0]]
                        if self.tabuleiro[destino[1]][destino[0]] == 0:
                            direcao = -1 if peca == 1 else 1
                            if destino[1] == origem[1] + direcao and abs(destino[0] - origem[0]) == 1:
                                self.tabuleiro[destino[1]][destino[0]] = peca
                                self.tabuleiro[origem[1]][origem[0]] = 0
                                print(f"✅ Peça movida de {origem} para {destino}")
                            else:
                                print("❌ Movimento inválido")
                        else:
                            print("❌ Destino ocupado")
                        self.posicao_destacada = None

            self.desenhar_tabuleiro()

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = VoiceControlledCheckers()
    app.iniciar()
