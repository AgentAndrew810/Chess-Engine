units_in_width = 20
units_in_height = 12
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
        cls.x_padd = cls.unit * 3 + (screen_width - width) // 2
        cls.y_padd = cls.unit * 2 + (screen_height - height) // 2

        # if a child object has an update method call it
        for child in cls._instances:
            if hasattr(child, "update"):
                child.update()
