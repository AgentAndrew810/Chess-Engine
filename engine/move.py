import utils


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
        def chess_position(pos) -> str:
            files = "abcdefgh"
            ranks = "87654321"
            rank, file = utils.get_coords(pos)
            return files[file] + ranks[rank]

        return chess_position(self.pos) + chess_position(self.dest) + self.prom
