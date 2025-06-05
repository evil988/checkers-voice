# menu/menu.py

import pygame
import sys
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# (Reaproveitamos constantes de cores e dimensões, ou podemos importá-las de checkers/draw.py)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
WIDTH, HEIGHT = 640, 640
MARGIN = 40

def init_menu_recognizer():
    path = os.path.join('assets', 'model')
    if not os.path.isdir(path):
        sys.exit(1)
    model = Model(path)
    cmds = json.dumps(['um jogador', 'dois jogadores', 'sair'])
    return KaldiRecognizer(model, 16000, cmds)

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
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192
    )
    stream.start_stream()

    hovered = None
    while True:
        window.fill(BLACK)
        # Cores dos itens destacados
        colors = [GREEN if hovered == i else WHITE for i in (1, 2, 3)]
        texts = ['1 Jogador', '2 Jogadores', 'Sair']
        rects = []

        for idx, txt in enumerate(texts, 1):
            surf = font.render(txt, True, colors[idx - 1])
            r = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (idx - 2) * 60))
            window.blit(surf, r)
            rects.append(r)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stream.stop_stream(); stream.close(); pa.terminate()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                hovered = next((i for i, r in enumerate(rects, 1) if r.collidepoint(event.pos)), None)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selection = next((i for i, r in enumerate(rects, 1) if r.collidepoint(event.pos)), None)
                if selection in (1, 2):
                    stream.stop_stream(); stream.close(); pa.terminate()
                    return selection
                if selection == 3:
                    pygame.quit(); sys.exit()

        data = stream.read(8192, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            txt = json.loads(recognizer.Result()).get('text', '').strip()
            if txt in ['um jogador', 'dois jogadores', 'sair']:
                stream.stop_stream(); stream.close(); pa.terminate()
                if txt == 'sair':
                    pygame.quit()
                    sys.exit()
                return 1 if txt == 'um jogador' else 2
