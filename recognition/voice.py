import os, sys, json, pyaudio
from vosk import Model, KaldiRecognizer

# Palavras que queremos reconhecer
numeros = ['um', 'dois', 'tres', 'três', 'quatro', 'cinco', 'seis', 'sete', 'oito']
ordinais = ['primeira', 'segunda', 'terceira', 'quarta', 'quinta', 'sexta', 'setima', 'sétima', 'oitava']
eixos = ['linha', 'coluna']

# Gera combinações válidas de frases
frases_validas = []
for linha in numeros + ordinais:
    for coluna in numeros + ordinais:
        frases_validas.append(f"linha {linha} coluna {coluna}")
        frases_validas.append(f"{linha} linha {coluna} coluna")

# Define gramática como frases completas
grammar = json.dumps(frases_validas)

# Caminho do modelo Vosk
model_path = "assets/model"
if not os.path.exists(model_path):
    print("Baixe um modelo do Vosk e coloque em 'assets/model'")
    sys.exit(1)

# Inicializa Vosk
model = Model(model_path)
rec = KaldiRecognizer(model, 16000, grammar)

# Configura microfone
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
