units_in_width = 14.5
units_in_height = 11
ratio = units_in_width / units_in_height


class DrawnObject:
    _instances = []

    def __init__(self) -> None:
        self._instances.append(self)

    @classmethod
    def set_sizes(cls, screen_width: int, screen_height: int) -> None:
        cls.screen_width = screen_width
        cls.screen_height = screen_height

        # if the width/height > ratio, use height to calculate width
        if screen_width / screen_height > ratio:
            height = screen_height
            width = round(height * ratio)
        # otherwise use width to calculate height
        else:
            width = screen_width
            height = round(width / ratio)

        # the size of one unit - this is the size used to determine where to place things on the gui
        # a square on the chess board is unit x unit
        cls.unit = round(width / units_in_width)

        # calculate padding
        # if width or height is too big, the other dimension gets more padding
        cls.x_padd = cls.unit // 2 + (screen_width - width) // 2
        cls.y_padd = cls.unit // 2 + (screen_height - height) // 2

        # determine chess board sizes
        cls.square_size = cls.unit
        cls.board_size = cls.unit * 8
        cls.profile_icon_size = cls.unit
        cls.board_start_x = cls.x_padd
        cls.board_end_x = cls.board_start_x + cls.board_size
        cls.board_start_y = cls.y_padd + cls.profile_icon_size
        cls.board_end_y = cls.board_start_y + cls.board_size

        cls.line_size = round(cls.unit / 20)
        cls.piece_size = cls.square_size - cls.line_size * 2

        # if a child object has an update method call it
        for child in cls._instances:
            if hasattr(child, "update"):
                child.update()