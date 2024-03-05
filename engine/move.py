class Move:
    def __init__(
        self, pos: int, dest: int, capture: bool, promotion: bool = False
    ) -> None:
        self.pos = pos
        self.dest = dest
        self.capture = capture
        self.promotion = promotion
