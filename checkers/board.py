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
        self.grid = [[0] * 8 for _ in range(8)]
        self._initialize_pieces()

    def _initialize_pieces(self):
        # Preenche as três primeiras camadas com peças azuis
        for y in range(3):
            for x in range(8):
                if (x + y) % 2 == 1:
                    self.grid[y][x] = 2
        # Preenche as três últimas camadas com peças vermelhas
        for y in range(5, 8):
            for x in range(8):
                if (x + y) % 2 == 1:
                    self.grid[y][x] = 1

    def reset(self):
        """
        Reinicia o tabuleiro ao estado inicial.
        """
        self.grid = [[0] * 8 for _ in range(8)]
        self._initialize_pieces()

    def get_piece(self, x, y):
        return self.grid[y][x]

    def set_piece(self, x, y, value):
        self.grid[y][x] = value

    def is_empty(self, x, y):
        return self.grid[y][x] == 0

    def all_pieces(self):
        return self.grid

    # Opcional: método que devolve uma cópia se precisar de estado separado
    def copy_board(self):
        return [row.copy() for row in self.grid]
