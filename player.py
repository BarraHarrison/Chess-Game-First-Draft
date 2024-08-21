class Player:
    def __init__(self, color):
        self.color = color

    def make_move(self, board):
        move = input(f"{self.color.capitalize()} player, enter your move: ")
        return move
