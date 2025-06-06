# checkers/board.py

"""Estruturas e utilidades do tabuleiro de damas."""

# Casa vazia
EMPTY = 0
# Peças normais
RED_PAWN = 1
BLUE_PAWN = 2
# Damas
RED_KING = 3
BLUE_KING = 4

# Tamanho padrão do tabuleiro (8x8)
BOARD_SIZE = 8
# Cada jogador começa com três linhas de peças
INITIAL_ROWS = 3


class Board:
    """Representa o estado do tabuleiro de damas."""

    def __init__(self):
        # Matriz 8x8 preenchida com EMPTY
        self.grid = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._initialize_pieces()

    def _initialize_pieces(self):
        """Posiciona as peças iniciais no tabuleiro."""
        # Região superior com peças azuis
        for y in range(INITIAL_ROWS):
            for x in range(BOARD_SIZE):
                if (x + y) % 2 == 1:
                    self.grid[y][x] = BLUE_PAWN
        # Região inferior com peças vermelhas
        for y in range(BOARD_SIZE - INITIAL_ROWS, BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if (x + y) % 2 == 1:
                    self.grid[y][x] = RED_PAWN

    def reset(self):
        """
        Reinicia o tabuleiro ao estado inicial.
        """
        self.grid = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self._initialize_pieces()

    def get_piece(self, x, y):
        """Retorna o valor armazenado na posição (x, y)."""
        return self.grid[y][x]

    def set_piece(self, x, y, value):
        """Define o valor da posição (x, y) para `value`."""
        self.grid[y][x] = value

    def is_empty(self, x, y):
        """Retorna ``True`` se a casa estiver vazia."""
        return self.grid[y][x] == EMPTY

    def all_pieces(self):
        """Retorna a matriz completa representando o tabuleiro."""
        return self.grid

    # Opcional: método que devolve uma cópia se precisar de estado separado
    def copy_board(self):
        """Retorna uma cópia independente do tabuleiro."""
        return [row.copy() for row in self.grid]
