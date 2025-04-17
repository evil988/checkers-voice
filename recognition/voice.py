
import os, sys, json, pyaudio
from vosk import Model, KaldiRecognizer

acao = ['mover', 'para']
posicaoA = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito']
posicaoB = ['primeira', 'segunda', 'terceira', 'quarta', 'quinta', 'sexta', 'setima', 'oitava']
orientacao = ['linha', 'coluna']

words = acao + posicaoA + posicaoB + orientacao + ['confirmar', 'desistir', 'cancelar']
grammar = json.dumps(words)

model_path = "assets/model"
if not os.path.exists(model_path):
    print("Baixe um modelo do Vosk e coloque em 'assets/model'")
    sys.exit(1)

model = Model(model_path)
rec = KaldiRecognizer(model, 16000, grammar)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

def escutar_comando():
    data = stream.read(8192, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        texto = result.get("text", "")
        return texto
    return None
