class Move:
    def __init__(
        self,
        pos: int,
        dest: int,
        capture: bool = False,
        castling: str = "",
        prom: str = "",
    ) -> None:
        self.pos = pos
        self.dest = dest
        self.capture = capture
        self.castling = castling
