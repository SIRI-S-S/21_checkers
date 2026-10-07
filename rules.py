SIZE = 8


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    if board[er][ec] != ".":
        return False

    piece = board[sr][sc]

    if piece not in (player, player + "K"):
        return False

    if abs(er - sr) != 1 or abs(ec - sc) != 1:
        return False

    # Kings can move in both directions.
    if piece == player + "K":
        return True

    # Normal pieces move only toward the opponent's side.
    direction = -1 if player == "R" else 1
    return er - sr == direction


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    if not (0 <= er < SIZE and 0 <= ec < SIZE):
        return False

    if board[er][ec] != ".":
        return False

    piece = board[sr][sc]

    if piece not in (player, player + "K"):
        return False

    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return False

    # Normal pieces can capture only forward.
    if piece == player:
        direction = -1 if player == "R" else 1
        if er - sr != 2 * direction:
            return False

    # Kings can capture in both directions.

    mr = (sr + er) // 2
    mc = (sc + ec) // 2

    return board[mr][mc] not in (".", player, player + "K")


def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"