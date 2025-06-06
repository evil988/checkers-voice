# menu/menu.py

import pygame
import sys
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

"""Menu principal do jogo controlado por voz ou mouse."""

# Cores e dimensões básicas (reaproveitadas em outros módulos)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
WIDTH, HEIGHT = 640, 640
MARGIN = 40

# Textos exibidos nas opções do menu
MENU_TEXTS = ['1 Jogador', '2 Jogadores', 'Sair']

# Comandos válidos reconhecidos pelo Vosk
VOICE_COMMANDS = ['um jogador', 'dois jogadores', 'sair']

def init_menu_recognizer():
    """Inicializa o reconhecedor de voz para os comandos do menu."""
    path = os.path.join('assets', 'model')
    if not os.path.isdir(path):
        sys.exit(1)

    model = Model(path)
    grammar = json.dumps(VOICE_COMMANDS)
    return KaldiRecognizer(model, 16000, grammar)


def open_audio_stream(pa):
    """Abre e inicia um stream de áudio para captura do microfone."""
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192,
    )
    stream.start_stream()
    return stream


def close_audio(stream, pa):
    """Encerra o stream de áudio com segurança."""
    stream.stop_stream()
    stream.close()
    pa.terminate()


def draw_options(window, font, hovered):
    """Desenha as opções do menu e retorna a lista de retângulos."""
    window.fill(BLACK)
    colors = [GREEN if hovered == i else WHITE for i in (1, 2, 3)]
    rects = []
    for idx, txt in enumerate(MENU_TEXTS, 1):
        surf = font.render(txt, True, colors[idx - 1])
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (idx - 2) * 60))
        window.blit(surf, rect)
        rects.append(rect)
    pygame.display.flip()
    return rects


def read_voice_command(stream, recognizer):
    """Lê áudio do microfone e retorna um comando válido ou ``None``."""
    data = stream.read(8192, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        text = json.loads(recognizer.Result()).get('text', '').strip()
        if text in VOICE_COMMANDS:
            return text
    return None

def show_menu():
    """
    Exibe o menu principal, aguardando clique ou comando de voz.
    Retorna 1 (um jogador), 2 (dois jogadores) ou sai do programa.
    """
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Damas - Menu')
    font = pygame.font.SysFont(None, 60)

    recognizer = init_menu_recognizer()
    pa = pyaudio.PyAudio()
    stream = open_audio_stream(pa)

    hovered = None
    while True:
        rects = draw_options(window, font, hovered)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_audio(stream, pa)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                hovered = next(
                    (i for i, r in enumerate(rects, 1) if r.collidepoint(event.pos)),
                    None,
                )

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selection = next(
                    (i for i, r in enumerate(rects, 1) if r.collidepoint(event.pos)),
                    None,
                )
                if selection in (1, 2):
                    close_audio(stream, pa)
                    return selection
                if selection == 3:
                    pygame.quit()
                    sys.exit()

        cmd = read_voice_command(stream, recognizer)
        if cmd:
            close_audio(stream, pa)
            if cmd == 'sair':
                pygame.quit()
                sys.exit()
            return 1 if cmd == 'um jogador' else 2
