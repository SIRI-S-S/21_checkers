from board import initial_board, move_piece, SIZE
from rules import simple_move, capture_move, promote


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    # Task 2: Check whether a player still has pieces
    def has_pieces(self, player):
        return any(
            cell in (player, player + "K")
            for row in self.board
            for cell in row
        )

    # Task 2: Check whether a player has at least one legal move
    def has_legal_move(self, player):
        for sr in range(SIZE):
            for sc in range(SIZE):
                if self.board[sr][sc] not in (player, player + "K"):
                    continue

                for er in range(SIZE):
                    for ec in range(SIZE):
                        if capture_move(
                            self.board,
                            player,
                            (sr, sc),
                            (er, ec)
                        ):
                            return True

                        if simple_move(
                            self.board,
                            player,
                            (sr, sc),
                            (er, ec)
                        ):
                            return True

        return False

    # Task 2: Check whether the game is over
    def game_over(self):
        for player, name in [("R", "Red"), ("B", "Blue")]:
            if not self.has_pieces(player) or not self.has_legal_move(player):
                winner = "Blue" if player == "R" else "Red"
                print(f"Game Over! {winner} wins.")
                return True

        return False

    # Task 3: Check whether a player has any capture available
    def has_any_capture(self, player):
        for sr in range(SIZE):
            for sc in range(SIZE):
                if self.board[sr][sc] not in (player, player + "K"):
                    continue

                for er in range(SIZE):
                    for ec in range(SIZE):
                        if capture_move(
                            self.board,
                            player,
                            (sr, sc),
                            (er, ec)
                        ):
                            return True

        return False

    # Task 3: Check whether the same piece can capture again
    def has_capture_from(self, player, start):
        sr, sc = start

        if self.board[sr][sc] not in (player, player + "K"):
            return False

        for er in range(SIZE):
            for ec in range(SIZE):
                if capture_move(
                    self.board,
                    player,
                    start,
                    (er, ec)
                ):
                    return True

        return False

    def run(self):
        print("Checkers — move: sr sc er ec")

        while True:
            self.print_board()

            if self.game_over():
                return

            player = self.player

            # Task 3: forced capture
            forced_capture = self.has_any_capture(player)

            raw = input(f"{player}> ").strip().lower().split()

            if raw == ["q"]:
                return

            if len(raw) != 4:
                print("Enter four coordinates.")
                continue

            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue

            if self.board[sr][sc] not in (player, player + "K"):
                print("That is not your piece.")
                continue

            start = (sr, sc)
            end = (er, ec)

            if forced_capture:
                if not capture_move(self.board, player, start, end):
                    print("You must capture when a capture is available.")
                    continue

                move_piece(self.board, start, end)

                was_promoted = self.board[end[0]][end[1]] == player
                promote(self.board)
                promoted = self.board[end[0]][end[1]] != player

                if promoted and not was_promoted:
                    print(f"Capture: {start} -> {end}; promoted to king.")
                else:
                    print(f"Capture: {start} -> {end}.")

                # Task 3: multi-capture
                current_position = end

                while self.has_capture_from(player, current_position):
                    self.print_board()

                    raw = input(f"{player} (continue capture)> ").strip().lower().split()

                    if raw == ["q"]:
                        return

                    if len(raw) != 4:
                        print("Enter four coordinates.")
                        continue

                    try:
                        csr, csc, cer, cec = map(int, raw)
                    except ValueError:
                        print("Coordinates must be numbers.")
                        continue

                    if not all(0 <= x < SIZE for x in (csr, csc, cer, cec)):
                        print("Outside board.")
                        continue

                    if (csr, csc) != current_position:
                        print("You must continue capturing with the same piece.")
                        continue

                    capture_start = current_position
                    capture_end = (cer, cec)

                    if not capture_move(
                        self.board,
                        player,
                        capture_start,
                        capture_end
                    ):
                        print("You must make another capture with this piece.")
                        continue

                    move_piece(
                        self.board,
                        capture_start,
                        capture_end
                    )

                    before_promotion = self.board[capture_end[0]][capture_end[1]]
                    promote(self.board)
                    promoted = (
                        self.board[capture_end[0]][capture_end[1]]
                        != before_promotion
                    )

                    if promoted:
                        print(
                            f"Capture: {capture_start} -> {capture_end}; "
                            f"promoted to king."
                        )
                    else:
                        print(f"Capture: {capture_start} -> {capture_end}.")

                    current_position = capture_end

                self.player = "B" if self.player == "R" else "R"
                continue

            # No capture is available, so a normal move or capture is allowed.
            if capture_move(self.board, player, start, end):
                move_piece(self.board, start, end)

                before_promotion = self.board[end[0]][end[1]]
                promote(self.board)
                promoted = self.board[end[0]][end[1]] != before_promotion

                if promoted:
                    print(f"Capture: {start} -> {end}; promoted to king.")
                else:
                    print(f"Capture: {start} -> {end}.")

            elif simple_move(self.board, player, start, end):
                move_piece(self.board, start, end)

                before_promotion = self.board[end[0]][end[1]]
                promote(self.board)
                promoted = self.board[end[0]][end[1]] != before_promotion

                if promoted:
                    print(f"Move: {start} -> {end}; promoted to king.")
                else:
                    print(f"Move: {start} -> {end}.")
            else:
                print("Invalid move.")
                continue

            self.player = "B" if self.player == "R" else "R"