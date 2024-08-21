from chess_pieces import Pawn, Rook, Knight, Bishop, Queen, King

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def setup_board(self):
        # Set up white pieces
        for i in range(8):
            self.board[1][i] = Pawn("white")  # White pawns
        self.board[0][0] = Rook("white")  # White rooks
        self.board[0][7] = Rook("white")
        self.board[0][1] = Knight("white")  # White knights
        self.board[0][6] = Knight("white")
        self.board[0][2] = Bishop("white")  # White bishops
        self.board[0][5] = Bishop("white")
        self.board[0][3] = Queen("white")  # White queen
        self.board[0][4] = King("white")  # White king

        # Set up black pieces
        for i in range(8):
            self.board[6][i] = Pawn("black")  # Black pawns
        self.board[7][0] = Rook("black")  # Black rooks
        self.board[7][7] = Rook("black")
        self.board[7][1] = Knight("black")  # Black knights
        self.board[7][6] = Knight("black")
        self.board[7][2] = Bishop("black")  # Black bishops
        self.board[7][5] = Bishop("black")
        self.board[7][3] = Queen("black")  # Black queen
        self.board[7][4] = King("black")  # Black king

    def display_board(self):
        for row in self.board:
            print(" ".join([str(piece) if piece else "." for piece in row]))

    def move_piece(self, move):
        try:
            start_pos, end_pos = move.split()
            start_row, start_col = self._parse_position(start_pos)
            end_row, end_col = self._parse_position(end_pos)

            piece = self.board[start_row][start_col]
            if piece and piece.is_valid_move(start_row, start_col, end_row, end_col, self.board):
                self.board[end_row][end_col] = piece
                self.board[start_row][start_col] = None
                return True
            else:
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def _parse_position(self, pos):
        row = 8 - int(pos[1])
        col = ord(pos[0]) - ord('a')
        return row, col
