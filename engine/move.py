class Move:
    def __init__( self, pos: int, dest: int, capture: bool) -> None:
        self.pos = pos
        self.dest = dest
        self.capture = capture
