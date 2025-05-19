import pygame
import sys
import os
import json
import random
import pyaudio
from vosk import Model, KaldiRecognizer

pygame.init()
LARGURA, ALTURA = 640, 640
TAMANHO_CASA = LARGURA // 8
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Damas - Controle por Voz e Mouse")

def mostrar_menu():
    fonte = pygame.font.SysFont(None, 60)
    comandos = json.dumps(["um jogador", "dois jogadores", "sair"])
    model_path = os.path.join("assets", "model")
    if not os.path.exists(model_path):
        sys.exit(1)
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000, comandos)
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    hovered = None
    while True:
        janela.fill(PRETO)
        cor1 = VERDE if hovered == 1 else BRANCO
        cor2 = VERDE if hovered == 2 else BRANCO
        cor3 = VERDE if hovered == 3 else BRANCO
        opc1 = fonte.render("1 Jogador", True, cor1)
        opc2 = fonte.render("2 Jogadores", True, cor2)
        opc3 = fonte.render("Sair", True, cor3)
        r1 = opc1.get_rect(center=(LARGURA//2, ALTURA//2 - 60))
        r2 = opc2.get_rect(center=(LARGURA//2, ALTURA//2))
        r3 = opc3.get_rect(center=(LARGURA//2, ALTURA//2 + 60))
        janela.blit(opc1, r1)
        janela.blit(opc2, r2)
        janela.blit(opc3, r3)
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                stream.stop_stream()
                stream.close()
                audio.terminate()
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEMOTION:
                x, y = e.pos
                if r1.collidepoint(x, y):
                    hovered = 1
                elif r2.collidepoint(x, y):
                    hovered = 2
                elif r3.collidepoint(x, y):
                    hovered = 3
                else:
                    hovered = None
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if r1.collidepoint(x, y):
                    choice = 1
                elif r2.collidepoint(x, y):
                    choice = 2
                elif r3.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()
                else:
                    continue
                stream.stop_stream()
                stream.close()
                audio.terminate()
                return choice
        # Depuração: leitura de áudio para menu
        data = stream.read(8192, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            text = json.loads(recognizer.Result()).get("text", "").strip()
            # Depuração: comando de menu reconhecido: text
            if text in ["um jogador", "dois jogadores", "sair"]:
                stream.stop_stream()
                stream.close()
                audio.terminate()
                if text == "sair":
                    pygame.quit()
                    sys.exit()
                return 1 if text == "um jogador" else 2

class VoiceMouseControlledCheckers:
    def __init__(self, mode):
        self.mode = mode
        self.numeros = ['um','dois','tres','quatro','cinco','seis','sete','oito']
        frases = [f"linha {l} coluna {c}" for l in self.numeros for c in self.numeros] + ["cancelar", "reiniciar", "voltar ao menu principal"]
        model = Model(os.path.join("assets","model"))
        self.recognizer = KaldiRecognizer(model, 16000, json.dumps(frases))
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()
        self.inicializar_tabuleiro()
        self.posicao_destacada = None
        self.rodando = True

    def inicializar_tabuleiro(self):
        self.tabuleiro = [[0]*8 for _ in range(8)]
        for y in range(3):
            for x in range(8):
                if (x+y)%2:
                    self.tabuleiro[y][x] = 2
        for y in range(5,8):
            for x in range(8):
                if (x+y)%2:
                    self.tabuleiro[y][x] = 1

    def desenhar_tabuleiro(self):
        for y in range(8):
            for x in range(8):
                cor = BRANCO if (x+y)%2==0 else PRETO
                pygame.draw.rect(janela, cor, (x*TAMANHO_CASA, y*TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA))
                if self.posicao_destacada == (x,y):
                    pygame.draw.rect(janela, VERDE, (x*TAMANHO_CASA, y*TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA), 4)
                p = self.tabuleiro[y][x]
                if p in (1,3):
                    pygame.draw.circle(janela, VERMELHO, (x*TAMANHO_CASA+TAMANHO_CASA//2, y*TAMANHO_CASA+TAMANHO_CASA//2), TAMANHO_CASA//2-10)
                elif p in (2,4):
                    pygame.draw.circle(janela, AZUL, (x*TAMANHO_CASA+TAMANHO_CASA//2, y*TAMANHO_CASA+TAMANHO_CASA//2), TAMANHO_CASA//2-10)
                if p in (3,4):
                    d = pygame.font.SysFont(None, TAMANHO_CASA//2).render("D", True, AMARELO)
                    rd = d.get_rect(center=(x*TAMANHO_CASA+TAMANHO_CASA//2, y*TAMANHO_CASA+TAMANHO_CASA//2))
                    janela.blit(d, rd)
        pygame.display.flip()

    def escutar_comando(self):
        # Depuração: leitura de áudio para comando de jogo
        data = self.stream.read(8192, exception_on_overflow=False)
        if self.recognizer.AcceptWaveform(data):
            t = json.loads(self.recognizer.Result()).get("text","").strip()
            # Depuração: comando reconhecido: t
            if t in ["cancelar","reiniciar","voltar ao menu principal"]:
                return "menu" if t=="voltar ao menu principal" else t
            sp = t.split()
            if len(sp)==4 and sp[0]=="linha" and sp[2]=="coluna" and sp[1] in self.numeros and sp[3] in self.numeros:
                return (self.numeros.index(sp[1]), self.numeros.index(sp[3]))
        return None

    def executar_jogada_azul(self):
        movs=[]
        for y in range(8):
            for x in range(8):
                if self.tabuleiro[y][x]==2:
                    for dx in (-1,1):
                        nx,ny=x+dx,y+1
                        if 0<=nx<8 and 0<=ny<8 and self.tabuleiro[ny][nx]==0:
                            movs.append(((x,y),(nx,ny)))
                    for dx in (-2,2):
                        nx,ny=x+dx,y+2
                        mx,my=x+dx//2,y+1
                        if 0<=nx<8 and 0<=ny<8 and self.tabuleiro[ny][nx]==0 and self.tabuleiro[my][mx]==1:
                            movs.append(((x,y),(nx,ny)))
        # Depuração: movimentos IA candidatos: movs
        if movs:
            origem,destino=random.choice(movs)
            x0,y0=origem; x1,y1=destino
            if abs(x1-x0)==2:
                mx,my=(x0+x1)//2,(y0+y1)//2
                self.tabuleiro[my][mx]=0
                # Depuração: captura IA em mx,my
            self.tabuleiro[y1][x1]=2; self.tabuleiro[y0][x0]=0
            if y1==7:
                self.tabuleiro[y1][x1]=4
                # Depuração: IA promove peça a dama em (x1,y1)
            # Depuração: IA moveu de origem para destino

    def handle_move(self, comando):
        if comando=="cancelar" and self.posicao_destacada:
            # Depuração: comando cancelar recebido
            self.posicao_destacada=None
        elif comando=="reiniciar":
            # Depuração: comando reiniciar recebido
            self.inicializar_tabuleiro(); self.posicao_destacada=None
        elif comando=="menu":
            # Depuração: comando voltar ao menu recebido
            return "menu"
        elif isinstance(comando, tuple):
            r,c = comando
            if self.posicao_destacada is None:
                if self.tabuleiro[r][c]==0 or (self.mode==1 and self.tabuleiro[r][c] not in (1,3)):
                    return
                # Depuração: posição destacada para movimento: (c,r)
                self.posicao_destacada=(c,r)
            else:
                origx,origy=self.posicao_destacada
                destx,desty=c, r
                p=self.tabuleiro[origy][origx]
                dir = -1 if p in (1,3) else 1
                if self.tabuleiro[desty][destx]==0 and desty==origy+dir and abs(destx-origx)==1:
                    # Movimento simples executado
                    self.tabuleiro[desty][destx]=p; self.tabuleiro[origy][origx]=0
                    if p in (1,3) and desty==0:
                        self.tabuleiro[desty][destx]=3
                        # Depuração: promoção a dama para jogador em (destx,desty)
                    if p in (2,4) and desty==7:
                        self.tabuleiro[desty][destx]=4
                        # Depuração: promoção a dama para IA em (destx,desty)
                    if self.mode==1: self.executar_jogada_azul()
                elif self.tabuleiro[desty][destx]==0 and desty==origy+2*dir and abs(destx-origx)==2:
                    mx,my=(origx+destx)//2,(origy+desty)//2
                    if self.tabuleiro[my][mx] not in (p,0):
                        # Captura executada de (origx,origy) para (destx,desty)
                        self.tabuleiro[desty][destx]=p; self.tabuleiro[origy][origx]=0; self.tabuleiro[my][mx]=0
                        if p in (1,3) and desty==0:
                            self.tabuleiro[desty][destx]=3
                            # Depuração: promoção após captura para jogador em (destx,desty)
                        if p in (2,4) and desty==7:
                            self.tabuleiro[desty][destx]=4
                            # Depuração: promoção após captura para IA em (destx,desty)
                        if self.mode==1: self.executar_jogada_azul()
                # Limpa destaque após ação
                self.posicao_destacada=None

    def iniciar(self):
        while self.rodando:
            for e in pygame.event.get():
                if e.type==pygame.QUIT:
                    self.rodando=False
                elif e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
                    row,col=e.pos[1]//TAMANHO_CASA,e.pos[0]//TAMANHO_CASA
                    if self.handle_move((row,col))=="menu":
                        return "menu"
            cmd=self.escutar_comando()
            if cmd and self.handle_move(cmd)=="menu":
                return "menu"
            self.desenhar_tabuleiro()
        self.stream.stop_stream();self.stream.close();self.audio.terminate();pygame.quit();sys.exit()

if __name__=="__main__":
    while True:
        modo=mostrar_menu()
        if modo in (1,2):
            resultado=VoiceMouseControlledCheckers(modo).iniciar()
            if resultado=="menu":
                continue
            else:
                break
        else:
            break
