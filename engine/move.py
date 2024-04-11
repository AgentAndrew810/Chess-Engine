from .utils import get_square


class Move:
    __slots__ = "pos", "dest", "capture", "castling", "prom", "double", "ep"

    def __init__(
        self,
        pos: int,
        dest: int,
        capture: bool = False,
        castling: str = "",
        prom: str = "",
        double: bool = False,
        ep: int = 0,
    ) -> None:
        self.pos = pos
        self.dest = dest
        self.capture = capture
        self.castling = castling
        self.prom = prom
        self.double = double
        self.ep = ep

    def __repr__(self) -> str:
        return get_square(self.pos) + get_square(self.dest) + self.prom
