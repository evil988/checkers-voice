# checkers/rules.py

def simple_moves(board, x, y):
    """
    Retorna lista de duplas ((x0,y0), (x1,y1)) para movimentos simples (não-captura),
    considerando se é peça normal (1 ou 2) ou dama (3 ou 4).
    Tabuleiro é uma lista 8x8.
    """
    p = board[y][x]
    moves = []
    if p == 1:   # peça vermelha (sobe)
        direcoes = [(-1, -1), (1, -1)]
    elif p == 2: # peça azul (desce)
        direcoes = [(-1, 1), (1, 1)]
    elif p == 3: # dama vermelha
        direcoes = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    elif p == 4: # dama azul
        direcoes = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    else:
        return []

    for dx, dy in direcoes:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and board[ny][nx] == 0:
            moves.append(((x, y), (nx, ny)))
    return moves

def capture_moves(board, x, y):
    """
    Retorna lista de duplas ((x0,y0),(x2,y2)) correspondentes a capturas:
    verifica se há peça adversária no meio e casa final livre.
    """
    p = board[y][x]
    captures = []
    if p in (1, 2):
        dir_y = -1 if p == 1 else 1
        poss = [(-2, 2 * dir_y), (2, 2 * dir_y)]
        for dx, dy in poss:
            nx, ny = x + dx, y + dy
            mx, my = x + dx // 2, y + dy // 2
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board[my][mx] != 0 and (board[my][mx] % 2) != (p % 2) and board[ny][nx] == 0:
                    captures.append(((x, y), (nx, ny)))
    elif p in (3, 4):  # dama
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            nx, ny = x + dx, y + dy
            mx, my = x + dx // 2, y + dy // 2
            if 0 <= nx < 8 and 0 <= ny < 8:
                if board[my][mx] != 0 and (board[my][mx] % 2) != (p % 2) and board[ny][nx] == 0:
                    captures.append(((x, y), (nx, ny)))
    return captures

def apply_move(board, origin, destination):
    """
    Executa movimento simples ou captura.
    Retorna True se houve captura (para possivelmente continuar múltipla captura), caso contrário False.
    """
    x0, y0 = origin
    x1, y1 = destination
    p = board[y0][x0]
    # Verifica se é movimento de captura
    if abs(x1 - x0) == 2 and abs(y1 - y0) == 2:
        mx, my = (x0 + x1) // 2, (y0 + y1) // 2
        board[my][mx] = 0  # remoção da peça capturada
        board[y1][x1] = p
        board[y0][x0] = 0
        return True
    else:
        # Movimento simples
        board[y1][x1] = p
        board[y0][x0] = 0
        return False

def promote_piece(board, x, y):
    """
    Se a peça (1 ou 2) alcançou a última linha, promove para dama (3 ou 4).
    """
    p = board[y][x]
    if p == 1 and y == 0:
        board[y][x] = 3
        return True
    if p == 2 and y == 7:
        board[y][x] = 4
        return True
    return False
