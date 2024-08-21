import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Requires Pillow package
from chess_board import ChessBoard
from game import Game

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess")
        self.board = ChessBoard()
        self.game = Game()
        self.selected_piece = None
        self.images = {}
        self.load_images()  # Ensure this method call is correct
        self.create_board()

    def load_images(self):
        pieces = {
        "wP": "icons-white-pawn.png",
        "wR": "icons-white-rook.png",
        "wN": "icons-white-knight.png",
        "wB": "icons-white-bishop.png",
        "wQ": "icons-white-queen.png",
        "wK": "icons-white-king.png",
        "bP": "icons-black-pawn.png",
        "bR": "icons-black-rook.png",
        "bN": "icons-black-knight.png",
        "bB": "icons-black-bishop.png",
        "bQ": "icons-black-queen.png",
        "bK": "icons-black-king.png"
    }

    for piece, filename in pieces.items():
        try:
            image = Image.open(f"images/{filename}")
            image = image.resize((64, 64), Image.Resampling.LANCZOS)
            self.images[piece] = ImageTk.PhotoImage(image)
            print(f"Loaded {filename} successfully")
        except Exception as e:
            print(f"Failed to load {filename}: {e}")


    def create_board(self):
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                button = tk.Button(self.root, width=8, height=4, command=lambda r=row, c=col: self.on_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button
        self.update_board()

    def update_board(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece:
                    piece_symbol = str(piece)
                    if piece_symbol.islower():
                        piece_symbol = "b" + piece_symbol.upper()
                    else:
                        piece_symbol = "w" + piece_symbol.upper()
                    self.buttons[row][col].config(image=self.images[piece_symbol], state=tk.NORMAL)
                else:
                    self.buttons[row][col].config(image='', state=tk.NORMAL)

                # Color the board squares
                if (row + col) % 2 == 0:
                    self.buttons[row][col].config(bg="white")
                else:
                    self.buttons[row][col].config(bg="gray")

    def on_click(self, row, col):
        if self.selected_piece:
            self.move_piece(row, col)
        else:
            self.select_piece(row, col)

    def select_piece(self, row, col):
        piece = self.board.board[row][col]
        if piece and piece.color == self.game.players[self.game.current_turn].color:
            self.selected_piece = (row, col)
            self.highlight_selected(row, col)

    def move_piece(self, row, col):
        start_row, start_col = self.selected_piece
        move = f"{chr(start_col + ord('a'))}{8 - start_row} {chr(col + ord('a'))}{8 - row}"
        
        if self.board.move_piece(move):
            self.game.switch_turn()
            self.update_board()
            if self.game.is_in_check(self.game.players[self.game.current_turn].color):
                messagebox.showinfo("Check!", f"{self.game.players[self.game.current_turn].color.capitalize()} is in check!")
            if self.game.is_checkmate(self.game.players[self.game.current_turn].color):
                messagebox.showinfo("Checkmate!", f"Checkmate! {self.game.players[self.game.current_turn].color.capitalize()} loses!")
                self.root.quit()
            if self.game.is_stalemate(self.game.players[self.game.current_turn].color):
                messagebox.showinfo("Stalemate!", "Stalemate! The game is a draw.")
                self.root.quit()
        else:
            messagebox.showerror("Invalid Move", "This move is not valid. Please try again.")

        self.selected_piece = None
        self.highlight_selected(None, None)

    def highlight_selected(self, row, col):
        for r in range(8):
            for c in range(8):
                if (r, c) == (row, col):
                    self.buttons[r][c].config(bg="yellow")
                else:
                    if (r + c) % 2 == 0:
                        self.buttons[r][c].config(bg="white")
                    else:
                        self.buttons[r][c].config(bg="gray")

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
