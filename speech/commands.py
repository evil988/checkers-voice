# speech/commands.py

"""Parsers and constants used by the voice command system."""

# Words representing board coordinates.
NUMBER_WORDS = [
    "um",
    "dois",
    "tres",
    "quatro",
    "cinco",
    "seis",
    "sete",
    "oito",
]


class CommandParser:
    """Interpreta texto bruto do Vosk em ações do jogo."""

    def __init__(self):
        self.numbers = NUMBER_WORDS

    def parse_menu(self, text):
        """
        Retorna 1, 2 ou 'sair' se reconhecer comando de menu.
        """
        text = text.lower().strip()
        if text in ['um jogador', 'dois jogadores', 'sair']:
            return text
        return None

    def parse_move(self, text):
        """
        Se o texto for no formato “linha X coluna Y”, retorna (coluna_index, linha_index) como tupla.
        Exemplo: “linha dois coluna cinco” → (1, 4) [porque índice base 0]
        """
        if not text:
            return None

        sp = text.split()
        if len(sp) == 4 and sp[0] == 'linha' and sp[2] == 'coluna':
            try:
                r = self.numbers.index(sp[1])
                c = self.numbers.index(sp[3])
                return (c, r)
            except ValueError:
                return None
        if text in ['cancelar', 'reiniciar', 'voltar ao menu principal']:
            return text  # ação especial
        return None
