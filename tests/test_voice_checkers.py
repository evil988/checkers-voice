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
pygame.display.set_caption("Damas - Controle por Voz e Mouse")


def mostrar_menu():
    fonte = pygame.font.SysFont(None, 60)
    comandos_menu = json.dumps(["um jogador", "dois jogadores", "sair"])
    model_path = os.path.join("assets", "model")
    if not os.path.exists(model_path):
        print("Modelo Vosk não encontrado. Coloque-o em 'assets/model'")
        sys.exit(1)
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000, comandos_menu)
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192
    )
    stream.start_stream()

    hovered = None

    while True:
        janela.fill(PRETO)
        cor1 = VERDE if hovered == 1 else BRANCO
        cor2 = VERDE if hovered == 2 else BRANCO
        cor3 = VERDE if hovered == 3 else BRANCO

        opcao1 = fonte.render("1 Jogador", True, cor1)
        opcao2 = fonte.render("2 Jogadores", True, cor2)
        opcao3 = fonte.render("Sair", True, cor3)

        rect1 = opcao1.get_rect(center=(LARGURA // 2, ALTURA // 2 - 60))
        rect2 = opcao2.get_rect(center=(LARGURA // 2, ALTURA // 2))
        rect3 = opcao3.get_rect(center=(LARGURA // 2, ALTURA // 2 + 60))

        janela.blit(opcao1, rect1)
        janela.blit(opcao2, rect2)
        janela.blit(opcao3, rect3)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                stream.stop_stream()
                stream.close()
                audio.terminate()
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEMOTION:
                x, y = evento.pos
                if rect1.collidepoint(x, y):
                    hovered = 1
                elif rect2.collidepoint(x, y):
                    hovered = 2
                elif rect3.collidepoint(x, y):
                    hovered = 3
                else:
                    hovered = None
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = evento.pos
                if rect1.collidepoint(x, y):
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    return 1
                if rect2.collidepoint(x, y):
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    return 2
                if rect3.collidepoint(x, y):
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
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


class VoiceMouseControlledCheckers:
    def __init__(self, mode):
        self.mode = mode
        self.inicializar_tabuleiro()
        self.rodando = True
        self.posicao_destacada = None

        # Definição das frases válidas para voz
        self.numeros = [
            'um', 'dois', 'tres', 'quatro',
            'cinco', 'seis', 'sete', 'oito'
        ]
        frases_validas = [
            f"linha {l} coluna {c}"
            for l in self.numeros
            for c in self.numeros
        ] + ["cancelar", "reiniciar", "voltar ao menu principal"]
        grammar = json.dumps(frases_validas)

        model_path = os.path.join("assets", "model")
        if not os.path.exists(model_path):
            print("Modelo Vosk não encontrado. Coloque-o em 'assets/model'")
            sys.exit(1)
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000, grammar)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )
        self.stream.start_stream()

    def inicializar_tabuleiro(self):
        self.tabuleiro = [[0] * 8 for _ in range(8)]
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
                pygame.draw.rect(
                    janela,
                    cor,
                    (x * TAMANHO_CASA, y * TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA)
                )
                if self.posicao_destacada == (x, y):
                    pygame.draw.rect(
                        janela,
                        VERDE,
                        (x * TAMANHO_CASA, y * TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA),
                        4
                    )
                if self.tabuleiro[y][x] == 1:
                    pygame.draw.circle(
                        janela,
                        VERMELHO,
                        (x * TAMANHO_CASA + TAMANHO_CASA // 2, y * TAMANHO_CASA + TAMANHO_CASA // 2),
                        TAMANHO_CASA // 2 - 10
                    )
                elif self.tabuleiro[y][x] == 2:
                    pygame.draw.circle(
                        janela,
                        AZUL,
                        (x * TAMANHO_CASA + TAMANHO_CASA // 2, y * TAMANHO_CASA + TAMANHO_CASA // 2),
                        TAMANHO_CASA // 2 - 10
                    )
        pygame.display.flip()

    def escutar_comando(self):
        data = self.stream.read(8192, exception_on_overflow=False)
        if self.recognizer.AcceptWaveform(data):
            result = json.loads(self.recognizer.Result())
            text = result.get("text", "").strip()
            if text:
                if text in ["cancelar", "reiniciar", "voltar ao menu principal"]:
                    return "menu" if text == "voltar ao menu principal" else text
                pal = text.split()
                if len(pal) == 4 and pal[0] == "linha" and pal[2] == "coluna":
                    if pal[1] in self.numeros and pal[3] in self.numeros:
                        return (pal[1], pal[3])
        return None

    def executar_jogada_azul(self):
        movimentos = []
        for y in range(8):
            for x in range(8):
                if self.tabuleiro[y][x] == 2:
                    for dx in (-1, 1):
                        nx, ny = x + dx, y + 1
                        if 0 <= nx < 8 and 0 <= ny < 8 and self.tabuleiro[ny][nx] == 0:
                            movimentos.append(((x, y), (nx, ny)))
                    for dx in (-2, 2):
                        nx, ny = x + dx, y + 2
                        mx, my = x + dx // 2, y + 1
                        if 0 <= nx < 8 and 0 <= ny < 8 and self.tabuleiro[ny][nx] == 0 and self.tabuleiro[my][mx] == 1:
                            movimentos.append(((x, y), (nx, ny)))
        if movimentos:
            origem, destino = random.choice(movimentos)
            x0, y0 = origem
            x1, y1 = destino
            if abs(x1 - x0) == 2:
                mx, my = (x0 + x1) // 2, (y0 + y1) // 2
                self.tabuleiro[my][mx] = 0
            self.tabuleiro[y1][x1] = 2
            self.tabuleiro[y0][x0] = 0
            print(f"🤖 Azul moveu de {origem} para {destino}")
        else:
            print("🤖 Azul sem jogadas possíveis")

    def handle_move(self, comando):
        # Comandos de controle
        if comando == "cancelar" and self.posicao_destacada:
            self.posicao_destacada = None
            print("✅ Destaque removido")
        elif comando == "reiniciar":
            self.inicializar_tabuleiro()
            self.posicao_destacada = None
            print("🔄 Jogo reiniciado")
        elif comando == "menu":
            return "menu"
        elif isinstance(comando, tuple):
            # Converte comandos de voz (strings) ou mouse (ínt).  
            if isinstance(comando[0], int):
                row_idx, col_idx = comando
            else:
                row_idx = self.numeros.index(comando[0])
                col_idx = self.numeros.index(comando[1])
            # Selecionar ou mover
            if self.posicao_destacada is None:
                if self.tabuleiro[row_idx][col_idx] == 0:
                    print("❌ Não há peça nessa posição")
                elif self.mode == 1 and self.tabuleiro[row_idx][col_idx] != 1:
                    print("❌ Modo 1 jogador: só peças vermelhas podem ser selecionadas")
                else:
                    self.posicao_destacada = (col_idx, row_idx)
                    print(f"🟩 Posição {self.posicao_destacada} destacada")
            else:
                origem = self.posicao_destacada
                destino = (col_idx, row_idx)
                peca = self.tabuleiro[origem[1]][origem[0]]
                # Movimento simples
                if self.tabuleiro[destino[1]][destino[0]] == 0 and destino[1] == origem[1] + (-1 if peca == 1 else 1) and abs(destino[0] - origem[0]) == 1:
                    self.tabuleiro[destino[1]][destino[0]] = peca
                    self.tabuleiro[origem[1]][origem[0]] = 0
                    print(f"✅ Peça movida de {origem} para {destino}")
                    if self.mode == 1:
                        self.executar_jogada_azul()
                # Captura
                elif self.tabuleiro[destino[1]][destino[0]] == 0 and destino[1] == origem[1] + 2 * (-1 if peca == 1 else 1) and abs(destino[0] - origem[0]) == 2:
                    meio_x = (origem[0] + destino[0]) // 2
                    meio_y = (origem[1] + destino[1]) // 2
                    if self.tabuleiro[meio_y][meio_x] != peca and self.tabuleiro[meio_y][meio_x] != 0:
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
        return None

    def iniciar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    x, y = evento.pos
                    col = x // TAMANHO_CASA
                    row = y // TAMANHO_CASA
                    resultado = self.handle_move((row, col))
                    if resultado == "menu":
                        return "menu"

            comando = self.escutar_comando()
            if comando:
                resultado = self.handle_move(comando)
                if resultado == "menu":
                    return "menu"

            self.desenhar_tabuleiro()

        # Cleanup
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    while True:
        modo = mostrar_menu()
        if modo in (1, 2):
            app = VoiceMouseControlledCheckers(modo)
            resultado = app.iniciar()
            if resultado == "menu":
                continue
            else:
                break
        else:
            break
