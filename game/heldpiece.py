class HeldPiece:
    def __init__(self) -> None:
        self.holding = False

    def grab(self, rank: int, file: int, piece: str) -> None:
        self.holding = True
        self.rank = rank
        self.file = file
        self.piece = piece

    def drop(self) -> None:
        self.holding = False

    @property
    def position(self) -> tuple[int, int]:
        return (self.rank, self.file) if self.holding else (-1, -1)