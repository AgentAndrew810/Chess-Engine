import engine
import utils


class HeldPiece:
    def __init__(self) -> None:
        self.drop()

    def grab(
        self, rank: int, file: int, piece: str, next_moves: list[engine.Move]
    ) -> None:
        self.holding = True
        self.rank = rank
        self.file = file
        self.piece = piece
        self.moves = [
            move.dest
            for move in next_moves
            if utils.get_coords(move.pos) == self.position
        ]

    def drop(self) -> None:
        self.holding = False
        self.moves = []

    @property
    def position(self) -> tuple[int, int]:
        return (self.rank, self.file) if self.holding else (-1, -1)
