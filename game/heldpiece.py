from engine import Move


class HeldPiece:
    def __init__(self) -> None:
        self.drop()

    def grab(self, pos: int, piece: str, next_moves: list[Move]) -> None:
        self.selected = True
        self.held = True

        self.pos = pos
        self.piece = piece
        self.moves = [move.dest for move in next_moves if move.pos == self.pos]

    def drop(self) -> None:
        self.selected = False
        self.held = False

        self.pos = None
        self.piece = ""
        self.moves = []
