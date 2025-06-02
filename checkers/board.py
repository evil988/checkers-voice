# checkers/board.py

class Board:
    """
    Representa o estado do tabuleiro de damas (8x8) e fornece métodos para inicializar e acessar.
    Valores:
      0 = casa vazia
      1 = peça vermelha
      2 = peça azul
      3 = dama vermelha
      4 = dama azul
    """

    def __init__(self):
        self.tabuleiro = [[0] * 8 for _ in range(8)]
        self._inicializar_peças()

    def _inicializar_peças(self):
        # Preenche as três primeiras camadas com peças azuis
        for y in range(3):
            for x in range(8):
                if (x + y) % 2 == 1:
                    self.tabuleiro[y][x] = 2
        # Preenche as três últimas camadas com peças vermelhas
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 == 1:
                    self.tabuleiro[y][x] = 1

    def reset(self):
        """
        Reinicia o tabuleiro ao estado inicial.
        """
        self.tabuleiro = [[0] * 8 for _ in range(8)]
        self._inicializar_peças()

    def get_piece(self, x, y):
        return self.tabuleiro[y][x]

    def set_piece(self, x, y, valor):
        self.tabuleiro[y][x] = valor

    def is_empty(self, x, y):
        return self.tabuleiro[y][x] == 0

    def all_pieces(self):
        return self.tabuleiro

    # Opcional: método que devolve uma cópia se precisar de estado separado
    def copy_board(self):
        return [linha.copy() for linha in self.tabuleiro]
