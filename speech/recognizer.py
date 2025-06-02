# speech/recognizer.py

import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

class SpeechRecognizer:
    """
    Encapsula a inicialização do Vosk e captura de pacotes de áudio.
    """

    def __init__(self, grammar_list):
        """
        grammar_list: lista de strings reconhecíveis (ex.: ['linha um coluna dois', ...])
        """
        model_path = os.path.join('assets', 'model')
        if not os.path.isdir(model_path):
            raise FileNotFoundError(f"Modelo Vosk não encontrado em {model_path}")

        self.model = Model(model_path)
        self.grammar = json.dumps(grammar_list)
        self.recognizer = KaldiRecognizer(self.model, 16000, self.grammar)
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )
        self.stream.start_stream()

    def read_audio(self):
        """
        Lê do buffer de áudio e retorna o texto reconhecido (ou vazio) no formato JSON do Vosk.
        """
        data = self.stream.read(8192, exception_on_overflow=False)
        if self.recognizer.AcceptWaveform(data):
            return json.loads(self.recognizer.Result()).get('text', '').strip()
        return ''

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
