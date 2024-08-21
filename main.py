from chess_board import ChessBoard

def main():
    board = ChessBoard()
    board.setup_board()

    while True:
        board.display_board()
        move = input("Enter your move (eg., e2 e4): ")
        if move.lower() == "exit":
            break

        if not board.move_piece(move):
            print("Invalid move. Try again.")

if __name__ == "__main__":
    main()