SIZE = 8


def initial_board():
    board = [["."] * SIZE for _ in range(SIZE)]
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"
    return board


def move_piece(board, start, end):
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = "."

    if abs(end[0] - start[0]) == 2 and abs(end[1] - start[1]) == 2:
        middle_row = (start[0] + end[0]) // 2
        middle_col = (start[1] + end[1]) // 2
        board[middle_row][middle_col] = "."