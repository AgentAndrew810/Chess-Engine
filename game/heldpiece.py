from .drawnobject import DrawnObject


class HeldPiece(DrawnObject):
    def __init__(self) -> None:
        super().__init__()
        self.drop()

    def grab(self, rank: int, file: int, piece: str) -> None:
        self.rank = rank
        self.file = file
        self.piece = piece

    def drop(self) -> None:
        self.rank = 0
        self.file = 0
        self.piece = ""
