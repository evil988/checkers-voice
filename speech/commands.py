# speech/commands.py

class CommandParser:
    """
    Interpreta texto bruto do Vosk em ações do jogo.
    """

    def __init__(self):
        self.numeros = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito']

    def parse_menu(self, texto):
        """
        Retorna 1, 2 ou 'sair' se reconhecer comando de menu.
        """
        texto = texto.lower().strip()
        if texto in ['um jogador', 'dois jogadores', 'sair']:
            return texto
        return None

    def parse_move(self, texto):
        """
        Se o texto for no formato “linha X coluna Y”, retorna (coluna_index, linha_index) como tupla.
        Exemplo: “linha dois coluna cinco” → (1, 4) [porque índice base 0]
        """
        if not texto:
            return None

        sp = texto.split()
        if len(sp) == 4 and sp[0] == 'linha' and sp[2] == 'coluna':
            try:
                r = self.numeros.index(sp[1])
                c = self.numeros.index(sp[3])
                return (c, r)
            except ValueError:
                return None
        if texto in ['cancelar', 'reiniciar', 'voltar ao menu principal']:
            return texto  # ação especial
        return None
