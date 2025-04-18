import os
import sys
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# =========================
# Configuração das frases válidas
# =========================
numbers = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito']
ordinals = ['primeira', 'segunda', 'terceira', 'quarta', 'quinta', 'sexta', 'setima', 'oitava']

valid_phrases = []
for row in numbers + ordinals:
    for col in numbers + ordinals:
        valid_phrases.append(f"linha {row} coluna {col}")
        valid_phrases.append(f"{row} linha {col} coluna")

grammar = json.dumps(valid_phrases)

# =========================
# Caminho do modelo Vosk
# =========================
model_path = os.path.join("assets", "model")
if not os.path.exists(model_path):
    print("Modelo Vosk não encontrado. Coloque-o em 'assets/model'")
    sys.exit(1)

# =========================
# Inicialização do Vosk e Microfone
# =========================
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000, grammar)

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)
stream.start_stream()

# =========================
# Loop de reconhecimento
# =========================
print("Fale algo como 'linha um coluna dois' ou 'segunda linha terceira coluna'...")

try:
    while True:
        data = stream.read(8192, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                print("✅ Comando reconhecido:", text)
except KeyboardInterrupt:
    print("\nEncerrando reconhecimento de voz.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
