# src/main.py

import sys
import os
import pygame

# Ajusta o path para permitir importar módulos de diretórios acima de 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from menu.menu import mostrar_menu
from speech.recognizer import SpeechRecognizer
from speech.commands import CommandParser
from checkers.board import Board
from checkers.rules import movimentos_simples, movimentos_captura, aplicar_movimento, promover_peça
from checkers.ai import escolher_jogada_aleatoria
from checkers.draw import desenhar_tabuleiro, LARGURA, ALTURA, MARGIN, TAMANHO_CASA

class VoiceMouseControlledCheckers:
    def __init__(self, mode):
        self.mode = mode  # 1 = um jogador, 2 = dois jogadores
        self.board = Board()
        self.posicao_destacada = None
        self.rodando = True

        numeros = ['um','dois','tres','quatro','cinco','seis','sete','oito']
        frases = [f'linha {l} coluna {c}' for l in numeros for c in numeros] + ['cancelar','reiniciar','voltar ao menu principal']
        self.speech_recognizer = SpeechRecognizer(frases)
        self.cmd_parser = CommandParser()

        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption('Damas - Controle por Voz e Mouse')

    def escutar_comando(self):
        texto = self.speech_recognizer.read_audio()
        if not texto:
            return None

        cmd_menu = self.cmd_parser.parse_menu(texto)
        if cmd_menu:
            return cmd_menu

        mov = self.cmd_parser.parse_move(texto)
        return mov

    def handle_move(self, comando):
        if comando == 'cancelar' and self.posicao_destacada:
            self.posicao_destacada = None

        elif comando == 'reiniciar':
            self.board.reset()
            self.posicao_destacada = None

        elif comando == 'voltar ao menu principal':
            return 'menu'

        elif isinstance(comando, tuple):
            c, r = comando
            x, y = c, r

            if self.posicao_destacada is None:
                p = self.board.get_piece(x, y)
                if p == 0 or (self.mode == 1 and p not in (1, 3)):
                    return
                self.posicao_destacada = (x, y)
                return

            ox, oy = self.posicao_destacada
            dest = (x, y)
            p = self.board.get_piece(ox, oy)

            caps = movimentos_captura(self.board.tabuleiro, ox, oy)
            if dest in [dest_pair[1] for dest_pair in caps]:
                aplicar_movimento(self.board.tabuleiro, (ox, oy), dest)
                promover_peça(self.board.tabuleiro, x, y)
                self.posicao_destacada = None
                if self.mode == 1:
                    self.jogada_ia()
                return

            sims = movimentos_simples(self.board.tabuleiro, ox, oy)
            if dest in [dest_pair[1] for dest_pair in sims]:
                aplicar_movimento(self.board.tabuleiro, (ox, oy), dest)
                promover_peça(self.board.tabuleiro, x, y)
                self.posicao_destacada = None
                if self.mode == 1:
                    self.jogada_ia()
                return

            return

    def jogada_ia(self):
        """
        Executa a jogada automática para o azul (modo 1), chamando função de IA.
        """
        resultado = escolher_jogada_aleatoria(self.board.tabuleiro)
        if resultado is None:
            return

        origem, destino, _ = resultado
        aplicar_movimento(self.board.tabuleiro, origem, destino)
        x, y = destino
        promover_peça(self.board.tabuleiro, x, y)


    def iniciar(self):
        clock = pygame.time.Clock()
        while self.rodando:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.rodando = False
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    pos_mouse = e.pos
                    col = (pos_mouse[0] - MARGIN) // TAMANHO_CASA
                    row = pos_mouse[1] // TAMANHO_CASA
                    if 0 <= col < 8 and 0 <= row < 8:
                        cmd = (col, row)
                        if self.handle_move(cmd) == 'menu':
                            return 'menu'

            cmd_voz = self.escutar_comando()
            if cmd_voz:
                if self.handle_move(cmd_voz) == 'menu':
                    return 'menu'

            desenhar_tabuleiro(self.janela, self.board.all_pieces(), self.posicao_destacada)
            clock.tick(30)

        self.speech_recognizer.close()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    while True:
        modo = mostrar_menu()
        if modo in (1, 2):
            resultado = VoiceMouseControlledCheckers(modo).iniciar()
            if resultado == 'menu':
                continue
            break
        else:
            break
