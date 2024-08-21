class ChessPiece:
    def __init__(self, color):
        self.color = color

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        raise NotImplementedError("This method should be implemented by subclasses")

    def is_opponent_piece(self, end_row, end_col, board):
        piece = board[end_row][end_col]
        return piece is not None and piece.color != self.color


class Pawn(ChessPiece):
    def __str__(self):
        return "P" if self.color == "white" else "p"

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        direction = 1 if self.color == "white" else -1
        start_row_initial = 1 if self.color == "white" else 6

        # Normal move
        if start_col == end_col and board[end_row][end_col] is None:
            if end_row == start_row + direction:
                return True
            if start_row == start_row_initial and end_row == start_row + 2 * direction and board[start_row + direction][end_col] is None:
                return True

        # Capture
        if abs(start_col - end_col) == 1 and end_row == start_row + direction and self.is_opponent_piece(end_row, end_col, board):
            return True

        return False


class Rook(ChessPiece):
    def __str__(self):
        return "R" if self.color == "white" else "r"

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        # Moving in a straight line (row or column)
        if start_row != end_row and start_col != end_col:
            return False

        # Moving vertically
        if start_col == end_col:
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] is not None:
                    return False

        # Moving horizontally
        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] is not None:
                    return False

        # Ensure not capturing own piece
        return not self.is_opponent_piece(end_row, end_col, board) or board[end_row][end_col] is None


class Knight(ChessPiece):
    def __str__(self):
        return "N" if self.color == "white" else "n"

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        # L-shape move: 2 squares in one direction and 1 in the other
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return not self.is_opponent_piece(end_row, end_col, board)

        return False


class Bishop(ChessPiece):
    def __str__(self):
        return "B" if self.color == "white" else "b"

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        # Moving diagonally
        if row_diff == col_diff:
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1

            for step in range(1, row_diff):
                if board[start_row + step * row_step][start_col + step * col_step] is not None:
                    return False

            return not self.is_opponent_piece(end_row, end_col, board)

        return False


class Queen(ChessPiece):
    def __str__(self):
        return "Q" if self.color == "white" else "q"

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        # Combine Rook and Bishop moves
        rook_like_move = Rook(self.color).is_valid_move(start_row, start_col, end_row, end_col, board)
        bishop_like_move = Bishop(self.color).is_valid_move(start_row, start_col, end_row, end_col, board)

        return rook_like_move or bishop_like_move


class King(ChessPiece):
    def __str__(self):
        return "K" if self.color == "white" else "k"

    def is_valid_move(self, start_row, start_col, end_row, end_col, board):
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        # King moves 1 square in any direction
        if row_diff <= 1 and col_diff <= 1:
            return not self.is_opponent_piece(end_row, end_col, board)

        return False
