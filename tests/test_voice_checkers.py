import pygame
import sys
import os
import json
import random
import pyaudio
from vosk import Model, KaldiRecognizer

pygame.init()
LARGURA, ALTURA = 640, 640
MARGIN = 40
TAMANHO_CASA = (LARGURA - MARGIN) // 8
BOARD_WIDTH = TAMANHO_CASA * 8
BOARD_HEIGHT = TAMANHO_CASA * 8

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Damas - Controle por Voz e Mouse')

def init_menu_recognizer():
    path = os.path.join('assets', 'model')
    if not os.path.isdir(path):
        sys.exit(1)
    model = Model(path)
    cmds = json.dumps(['um jogador', 'dois jogadores', 'sair'])
    return KaldiRecognizer(model, 16000, cmds)

def show_menu():
    fonte = pygame.font.SysFont(None, 60)
    recognizer = init_menu_recognizer()
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000,
                     input=True, frames_per_buffer=8192)
    stream.start_stream()
    hovered = None
    while True:
        window.fill(PRETO)
        cores = [VERDE if hovered == i else BRANCO for i in (1, 2, 3)]
        textos = ['1 Jogador', '2 Jogadores', 'Sair']
        rects = []
        for idx, txt in enumerate(textos, 1):
            surf = fonte.render(txt, True, cores[idx-1])
            r = surf.get_rect(center=(LARGURA//2, ALTURA//2 + (idx-2)*60))
            window.blit(surf, r)
            rects.append(r)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print('Exiting game')
                stream.stop_stream(); stream.close(); pa.terminate(); pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEMOTION:
                hovered = next((i for i, r in enumerate(rects, 1) if r.collidepoint(e.pos)), None)
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                sel = next((i for i, r in enumerate(rects, 1) if r.collidepoint(e.pos)), None)
                if sel in (1, 2):
                    print(f'Menu selected via mouse: {sel}')
                    stream.stop_stream(); stream.close(); pa.terminate(); return sel
                if sel == 3:
                    print('Menu selected via mouse: Sair')
                    pygame.quit(); sys.exit()
        data = stream.read(8192, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            txt = json.loads(recognizer.Result()).get('text', '').strip()
            print(f'Menu command recognized: {txt}')
            if txt in ['um jogador', 'dois jogadores', 'sair']:
                stream.stop_stream(); stream.close(); pa.terminate()
                if txt == 'sair': print('Menu command: sair'); pygame.quit(); sys.exit()
                print(f'Menu choice: {txt}'); return 1 if txt == 'um jogador' else 2

class VoiceMouseControlledCheckers:
    def __init__(self, mode):
        self.mode = mode
        self.numbers = ['um','dois','tres','quatro','cinco','seis','sete','oito']
        phrases = [f'linha {l} coluna {c}' for l in self.numbers for c in self.numbers] + ['cancelar','reiniciar','voltar ao menu principal']
        model = Model(os.path.join('assets','model'))
        self.recognizer = KaldiRecognizer(model, 16000, json.dumps(phrases))
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()
        self.inicializar_tabuleiro()
        self.highlighted_pos = None
        self.running = True

    def inicializar_tabuleiro(self):
        self.tabuleiro = [[0]*8 for _ in range(8)]
        for y in range(3):
            for x in range(8):
                if (x+y)%2: self.tabuleiro[y][x] = 2
        for y in range(5,8):
            for x in range(8):
                if (x+y)%2: self.tabuleiro[y][x] = 1
        print('Tabuleiro inicializado')

    def draw_board(self):
        fonte_label = pygame.font.SysFont(None, 24)
        window.fill(PRETO)
        for y in range(8):
            for x in range(8):
                cor = BRANCO if (x+y)%2==0 else PRETO
                rect = pygame.Rect(MARGIN+x*TAMANHO_CASA, y*TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA)
                pygame.draw.rect(window, cor, rect)
                if self.highlighted_pos == (x, y): pygame.draw.rect(window, VERDE, rect, 4)
                p = self.tabuleiro[y][x]
                center = (MARGIN + x*TAMANHO_CASA + TAMANHO_CASA//2, y*TAMANHO_CASA + TAMANHO_CASA//2)
                if p in (1,3): pygame.draw.circle(window, VERMELHO, center, TAMANHO_CASA//2-10)
                if p in (2,4): pygame.draw.circle(window, AZUL, center, TAMANHO_CASA//2-10)
                if p in (3,4):
                    d = pygame.font.SysFont(None, TAMANHO_CASA//2).render('D', True, AMARELO)
                    window.blit(d, d.get_rect(center=center))
        col_labels = ['C1','C2','C3','C4','C5','C6','C7','C8']
        for i,text in enumerate(col_labels):
            label = fonte_label.render(text, True, AMARELO)
            lx = MARGIN + i*TAMANHO_CASA + (TAMANHO_CASA-label.get_width())//2
            ly = BOARD_HEIGHT + (MARGIN-label.get_height())//2
            window.blit(label,(lx,ly))
        row_labels = ['L1','L2','L3','L4','L5','L6','L7','L8']
        for j,text in enumerate(row_labels):
            label = fonte_label.render(text,True,AMARELO)
            lx = (MARGIN-label.get_width())//2
            ly = j*TAMANHO_CASA + (TAMANHO_CASA-label.get_height())//2
            window.blit(label,(lx,ly))
        pygame.display.flip()

    def escutar_comando(self):
        data = self.stream.read(8192, exception_on_overflow=False)
        if self.recognizer.AcceptWaveform(data):
            txt = json.loads(self.recognizer.Result()).get('text','').strip()
            print(f'Comando reconhecido: {txt}')
            if txt in ['cancelar','reiniciar','voltar ao menu principal']:
                print(f'Ação de menu: {txt}'); return 'menu' if txt=='voltar ao menu principal' else txt
            sp = txt.split()
            if len(sp)==4 and sp[0]=='linha' and sp[2]=='coluna' and sp[1] in self.numbers and sp[3] in self.numbers:
                pos=(self.numbers.index(sp[1]),self.numbers.index(sp[3])); print(f'Posição escutada: {pos}'); return pos
        return None

    def executar_jogada_azul(self):
        movs=[]
        for y in range(8):
            for x in range(8):
                p=self.tabuleiro[y][x]
                if p==2:
                    for dx in(-1,1):
                        nx,ny=x+dx,y+1
                        if 0<=nx<8 and 0<=ny<8 and self.tabuleiro[ny][nx]==0: movs.append(((x,y),(nx,ny)))
                    for dx in(-2,2):
                        nx,ny=x+dx,y+2;mx,my=x+dx//2,y+1
                        if 0<=nx<8 and 0<=ny<8 and self.tabuleiro[ny][nx]==0 and self.tabuleiro[my][mx] in(1,3): movs.append(((x,y),(nx,ny)))
                if p==4:
                    for dx,dy in[(-1,-1),(-1,1),(1,-1),(1,1)]:
                        if 0<=x+dx<8 and 0<=y+dy<8 and self.tabuleiro[y+dy][x+dx]==0: movs.append(((x,y),(x+dx,y+dy)))
                    for dx,dy in[(-2,-2),(-2,2),(2,-2),(2,2)]:
                        mx,my=x+dx//2,y+dy//2;nx,ny=x+dx,y+dy
                        if 0<=nx<8 and 0<=ny<8 and self.tabuleiro[ny][nx]==0 and self.tabuleiro[my][mx] in(1,3): movs.append(((x,y),(nx,ny)))
        if movs:
            origem,destino=random.choice(movs);print(f'IA movendo de {origem} para {destino}')
            x0,y0=origem;x1,y1=destino;p=self.tabuleiro[y0][x0]
            if abs(x1-x0)==2:
                mx,my=(x0+x1)//2,(y0+y1)//2;self.tabuleiro[my][mx]=0;print(f'IA capturou em {(mx,my)}')
            self.tabuleiro[y1][x1]=p;self.tabuleiro[y0][x0]=0
            if p==2 and y1==7: self.tabuleiro[y1][x1]=4;print(f'IA promoveu peça em {(x1,y1)}')

    def handle_move(self, comando):
        if comando=='cancelar' and self.highlighted_pos:
            print('Comando: cancelar');self.highlighted_pos=None
        elif comando=='reiniciar':
            print('Comando: reiniciar');self.inicializar_tabuleiro();self.highlighted_pos=None
        elif comando=='menu':
            print('Comando: voltar ao menu');return 'menu'
        elif isinstance(comando,tuple):
            r,c=comando
            if self.highlighted_pos is None:
                if (self.tabuleiro[r][c] == 0 or
                    (self.mode == 1 and
                     self.tabuleiro[r][c] not in (1, 3))):
                    return
                print(f'Posição destacada para movimentação: {(c, r)}')
                self.highlighted_pos = (c, r)
                return
            ox, oy = self.highlighted_pos
            dx, dy = c - ox, r - oy
            p = self.tabuleiro[oy][ox]
            if p in (1, 2):
                dir_y = -1 if p == 1 else 1
                if abs(dx) == 1 and dy == dir_y and self.tabuleiro[r][c] == 0:
                    print(f'Movimento simples de {(ox, oy)} para {(c, r)}')
                    self.tabuleiro[r][c] = p
                    self.tabuleiro[oy][ox] = 0
                    self.highlighted_pos = None
                    if (p == 1 and r == 0) or (p == 2 and r == 7):
                        self.tabuleiro[r][c] = p + 2
                        print(f'Promoção em {(c, r)}')
                    if self.mode == 1:
                        self.executar_jogada_azul()
                elif abs(dx) == 2 and dy == 2*dir_y and self.tabuleiro[r][c] == 0:
                    mx, my = (ox + c)//2, (oy + r)//2
                    if self.tabuleiro[my][mx] not in (p, 0):
                        print(f'Captura de {(ox, oy)} para {(c, r)} removendo {(mx, my)}')
                        self.tabuleiro[my][mx] = 0
                        self.tabuleiro[r][c] = p
                        self.tabuleiro[oy][ox] = 0
                        self.highlighted_pos = None
                        if (p == 1 and r == 0) or (p == 2 and r == 7):
                            self.tabuleiro[r][c] = p + 2
                            print(f'Promoção após captura em {(c, r)}')
                        if self.mode == 1:
                            self.executar_jogada_azul()
            if p in (3, 4):
                if abs(dx) == 1 and abs(dy) == 1 and self.tabuleiro[r][c] == 0:
                    print(f'Dama movendo de {(ox, oy)} para {(c, r)}')
                    self.tabuleiro[r][c] = p
                    self.tabuleiro[oy][ox] = 0
                    self.highlighted_pos = None
                    if self.mode == 1:
                        self.executar_jogada_azul()
                    return
                if abs(dx) == 2 and abs(dy) == 2 and self.tabuleiro[r][c] == 0:
                    mx, my = (ox + c)//2, (oy + r)//2
                    if self.tabuleiro[my][mx] not in (p, 0):
                        print(f'Dama capturando de {(ox, oy)} para {(c, r)} removendo {(mx, my)}')
                        self.tabuleiro[my][mx] = 0
                        self.tabuleiro[r][c] = p
                        self.tabuleiro[oy][ox] = 0
                        captura_possivel = False
                        for ddx, ddy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                            nx, ny = c + ddx, r + ddy
                            mx2, my2 = c + ddx//2, r + ddy//2
                            if (0 <= nx < 8 and 0 <= ny < 8 and self.tabuleiro[ny][nx] == 0 and
                                self.tabuleiro[my2][mx2] in ((1, 3) if p == 4 else (2, 4))):
                                captura_possivel = True
                                break
                        if captura_possivel:
                            print(f'Dama múltipla captura continua em {(c, r)}')
                            self.highlighted_pos = (c, r)
                            return
                        self.highlighted_pos = None
                        if self.mode == 1:
                            self.executar_jogada_azul()

    def start(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    print('Encerrando jogo')
                    self.running = False
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    sel = ((e.pos[1] // TAMANHO_CASA),
                           ((e.pos[0] - MARGIN) // TAMANHO_CASA))
                    if self.handle_move(sel) == 'menu':
                        return 'menu'
            cmd = self.escutar_comando()
            if cmd and self.handle_move(cmd) == 'menu':
                return 'menu'
            self.draw_board()
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    while True:
        modo = show_menu()
        if modo in (1, 2):
            res = VoiceMouseControlledCheckers(modo).start()
            if res == 'menu':
                continue
            break
        else:
            break
