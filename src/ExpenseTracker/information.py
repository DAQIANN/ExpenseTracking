import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class UserInformation():
    def __init__(self, switch_to_main):
        super().__init__()

        self.label = toga.Label("Home Screen")
        self.add(self.label)

        self.switch_to_main = switch_to_main

        back_button = toga.Button(
            'Back',
            on_press=self.switch_to_main,
            style=Pack(padding=5)
        )
        self.add(back_button)