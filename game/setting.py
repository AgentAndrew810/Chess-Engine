from .radiobutton import RadioButton
from .drawnobject import DrawnObject


class Setting(DrawnObject):
    def __init__(self, buttons: list[RadioButton]) -> None:
        self.buttons = buttons

    def update_positions(self, group_num: int) -> None:
        # temp positions for buttons
        x = self.x_padd + self.unit * 6
        y = self.y_padd + round(self.unit * 2.5)
        radius = self.unit // 4

        for i, button in enumerate(self.buttons):
            button.resize((x + self.unit * 3 * i, y + self.unit * group_num), radius)

    def disable_all(self) -> None:
        for button in self.buttons:
            button.enabled = False

    def handle_click(self) -> None:
        # on a click go through every button and check if one is clicked
        # if one is clicked disabled all buttons except the clicked one
        for button in self.buttons:
            if button.is_over():
                self.disable_all()
                button.enabled = True
                break

    def value(self):
        for button in self.buttons:
            if button.enabled:
                return button.value

        return None
