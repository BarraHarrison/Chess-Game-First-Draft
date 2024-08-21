from chess_board import ChessBoard
from player import Player
from chess_pieces import King, Queen, Rook, Bishop, Knight, Pawn


class Game:
    def __init__(self):
        self.board = ChessBoard()
        self.players = [Player("white"), Player("black")]
        self.current_turn = 0  # 0 for white, 1 for black
        self.board.setup_board()

    def switch_turn(self):
        self.current_turn = 1 - self.current_turn

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece is not None and isinstance(piece, King) and piece.color == color:
                    return row, col
        return None

    def is_in_check(self, color):
        king_position = self.find_king(color)
        if king_position is None:
            return False
        
        king_row, king_col = king_position
        opponent_color = "black" if color == "white" else "white"

        # Check all opponent pieces to see if they can move to the king's position
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece is not None and piece.color == opponent_color:
                    if piece.is_valid_move(row, col, king_row, king_col, self.board.board):
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        # Try all possible moves to see if any of them removes the check
        for start_row in range(8):
            for start_col in range(8):
                piece = self.board.board[start_row][start_col]
                if piece is not None and piece.color == color:
                    for end_row in range(8):
                        for end_col in range(8):
                            original_piece = self.board.board[end_row][end_col]
                            if piece.is_valid_move(start_row, start_col, end_row, end_col, self.board.board):
                                self.board.board[end_row][end_col] = piece
                                self.board.board[start_row][start_col] = None
                                if not self.is_in_check(color):
                                    self.board.board[start_row][start_col] = piece
                                    self.board.board[end_row][end_col] = original_piece
                                    return False
                                self.board.board[start_row][start_col] = piece
                                self.board.board[end_row][end_col] = original_piece
        return True

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False

        # Check if any legal moves are available
        for start_row in range(8):
            for start_col in range(8):
                piece = self.board.board[start_row][start_col]
                if piece is not None and piece.color == color:
                    for end_row in range(8):
                        for end_col in range(8):
                            original_piece = self.board.board[end_row][end_col]
                            if piece.is_valid_move(start_row, start_col, end_row, end_col, self.board.board):
                                self.board.board[end_row][end_col] = piece
                                self.board.board[start_row][start_col] = None
                                if not self.is_in_check(color):
                                    self.board.board[start_row][start_col] = piece
                                    self.board.board[end_row][end_col] = original_piece
                                    return False
                                self.board.board[start_row][start_col] = piece
                                self.board.board[end_row][end_col] = original_piece
        return True

    def play(self):
        while True:
            self.board.display_board()
            current_player = self.players[self.current_turn]
            print(f"{current_player.color.capitalize()}'s turn")
            
            if self.is_checkmate(current_player.color):
                print(f"Checkmate! {current_player.color.capitalize()} loses!")
                break
            if self.is_stalemate(current_player.color):
                print("Stalemate! The game is a draw.")
                break

            move = current_player.make_move(self.board)

            if not self.board.move_piece(move):
                print("Invalid move. Try again.")
                continue

            if self.is_in_check(self.players[self.current_turn].color):
                print(f"{current_player.color.capitalize()} is in check!")

            self.switch_turn()

if __name__ == "__main__":
    game = Game()
    game.play()
