
from recognition.voice import escutar_comando
from game.checkers import CheckersGame
import time

jogo = CheckersGame()

# Inicia a interface gráfica em uma thread separada
import threading
threading.Thread(target=jogo.rodar_jogo, daemon=True).start()

print("Sistema iniciado. Diga o comando de voz...")

while True:
    comando = escutar_comando()
    if comando:
        print(f"Comando reconhecido: {comando}")
        jogo.mover_por_comando(comando)
    time.sleep(0.1)
