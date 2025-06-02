# menu/menu.py

import pygame
import sys
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# (Reaproveitamos constantes de cores e dimensões, ou podemos importá-las de checkers/draw.py)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
LARGURA, ALTURA = 640, 640
MARGIN = 40

def init_menu_recognizer():
    path = os.path.join('assets', 'model')
    if not os.path.isdir(path):
        sys.exit(1)
    model = Model(path)
    cmds = json.dumps(['um jogador', 'dois jogadores', 'sair'])
    return KaldiRecognizer(model, 16000, cmds)

def mostrar_menu():
    """
    Exibe o menu principal, aguardando clique ou comando de voz.
    Retorna 1 (um jogador), 2 (dois jogadores) ou sai do programa.
    """
    pygame.init()
    janela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption('Damas - Menu')
    fonte = pygame.font.SysFont(None, 60)

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
        janela.fill(PRETO)
        # Cores dos itens destacados
        cores = [VERDE if hovered == i else BRANCO for i in (1, 2, 3)]
        textos = ['1 Jogador', '2 Jogadores', 'Sair']
        rects = []

        for idx, txt in enumerate(textos, 1):
            surf = fonte.render(txt, True, cores[idx - 1])
            r = surf.get_rect(center=(LARGURA // 2, ALTURA // 2 + (idx - 2) * 60))
            janela.blit(surf, r)
            rects.append(r)

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                stream.stop_stream(); stream.close(); pa.terminate()
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEMOTION:
                hovered = next((i for i, r in enumerate(rects, 1) if r.collidepoint(e.pos)), None)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                sel = next((i for i, r in enumerate(rects, 1) if r.collidepoint(e.pos)), None)
                if sel in (1, 2):
                    stream.stop_stream(); stream.close(); pa.terminate()
                    return sel
                if sel == 3:
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
