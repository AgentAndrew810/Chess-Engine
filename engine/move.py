class Move:
    def __init__(
        self,
        pos: int,
        dest: int,
        capture: bool = False,
        castling: str = "",
        prom: str = "",
        double: bool = False,
        ep: bool = False,
    ) -> None:
        self.pos = pos
        self.dest = dest
        self.capture = capture
        self.castling = castling
        self.prom = prom
        self.double = double
        self.ep = ep
