# src/main.py

import sys
import os
import pygame

# Ajusta o path para permitir importar módulos de diretórios acima de 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from menu.menu import show_menu
from speech.recognizer import SpeechRecognizer
from speech.commands import CommandParser
from checkers.board import Board
from checkers.rules import (
    simple_moves,
    capture_moves,
    apply_move,
    promote_piece,
)
from checkers.opponent import choose_random_move
from checkers.draw import (
    draw_board,
    WIDTH,
    HEIGHT,
    MARGIN,
    SQUARE_SIZE,
)

class VoiceMouseControlledCheckers:
    def __init__(self, mode):
        self.mode = mode  # 1 = um jogador, 2 = dois jogadores
        self.board = Board()
        self.highlighted_pos = None
        self.running = True

        numbers = ['um','dois','tres','quatro','cinco','seis','sete','oito']
        phrases = [f'linha {l} coluna {c}' for l in numbers for c in numbers] + ['cancelar','reiniciar','voltar ao menu principal']
        model_path = os.environ.get('VOSK_MODEL_PATH')
        self.speech_recognizer = SpeechRecognizer(phrases, model_path=model_path)
        self.cmd_parser = CommandParser()

        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Damas - Controle por Voz e Mouse')

    def escutar_comando(self):
        text = self.speech_recognizer.read_audio()
        if not text:
            return None

        cmd_menu = self.cmd_parser.parse_menu(text)
        if cmd_menu:
            return cmd_menu

        mov = self.cmd_parser.parse_move(text)
        return mov

    def handle_move(self, comando):
        if comando == 'cancelar' and self.highlighted_pos:
            self.highlighted_pos = None

        elif comando == 'reiniciar':
            self.board.reset()
            self.highlighted_pos = None

        elif comando == 'voltar ao menu principal':
            return 'menu'

        elif isinstance(comando, tuple):
            c, r = comando
            x, y = c, r

            if self.highlighted_pos is None:
                p = self.board.get_piece(x, y)
                if p == 0 or (self.mode == 1 and p not in (1, 3)):
                    return
                self.highlighted_pos = (x, y)
                return

            ox, oy = self.highlighted_pos
            dest = (x, y)
            p = self.board.get_piece(ox, oy)

            caps = capture_moves(self.board.grid, ox, oy)
            if dest in [dest_pair[1] for dest_pair in caps]:
                apply_move(self.board.grid, (ox, oy), dest)
                promote_piece(self.board.grid, x, y)
                self.highlighted_pos = None
                if self.mode == 1:
                    self.ai_move()
                return

            sims = simple_moves(self.board.grid, ox, oy)
            if dest in [dest_pair[1] for dest_pair in sims]:
                apply_move(self.board.grid, (ox, oy), dest)
                promote_piece(self.board.grid, x, y)
                self.highlighted_pos = None
                if self.mode == 1:
                    self.ai_move()
                return

            return

    def ai_move(self):
        """
        Executa a jogada automática para o azul (modo 1), chamando função de IA.
        """
        result = choose_random_move(self.board.grid)
        if result is None:
            return

        origem, destino, _ = result
        apply_move(self.board.grid, origem, destino)
        x, y = destino
        promote_piece(self.board.grid, x, y)


    def start(self):
        clock = pygame.time.Clock()
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    pos_mouse = e.pos
                    col = (pos_mouse[0] - MARGIN) // SQUARE_SIZE
                    row = pos_mouse[1] // SQUARE_SIZE
                    if 0 <= col < 8 and 0 <= row < 8:
                        cmd = (col, row)
                        if self.handle_move(cmd) == 'menu':
                            return 'menu'

            voice_cmd = self.escutar_comando()
            if voice_cmd:
                if self.handle_move(voice_cmd) == 'menu':
                    return 'menu'

            draw_board(self.window, self.board.all_pieces(), self.highlighted_pos)
            clock.tick(30)

        self.speech_recognizer.close()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    while True:
        modo = show_menu()
        if modo in (1, 2):
            result = VoiceMouseControlledCheckers(modo).start()
            if result == 'menu':
                continue
            break
        else:
            break
