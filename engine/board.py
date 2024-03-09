DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"


class Board:
    def __init__(self, fen: str = DEFAULT_FEN) -> None:
        board = " " * 21
        for char in fen:
            if char.isdigit():
                board += "." * int(char)
            elif char == "/":
                board += " " * 2
                print(len(board))
            else:
                board += char
        board += " " * 21

        self.board = board
        self.white_move = True
