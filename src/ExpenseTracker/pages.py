import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.constants import CENTER
import os

from ExpenseTracker.json_backend import load_json, save_json_file
from ExpenseTracker.common import create_submit_button

class HomePage(toga.Box):
    def __init__(self, switch_to_main, main_window):
        super().__init__()

        self.switch_to_main = switch_to_main
        self.main_window = main_window

        box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        box.add(toga.Label('Welcome to Expense Tracker!', style=Pack(font_size=20, text_align='center')))

        bottom_right_box = toga.Box(style=Pack(direction='row', alignment='right'))
        spacer = toga.Box(style=Pack(flex=1))
        bottom_right_box.add(spacer)
        back_button = toga.Button(
            'Back',
            on_press=self.switch_to_main,
            style=Pack(padding=5)
        )

        top_box = toga.Box(
            toga.Label(
                "Please observe a sample cost input below : ",
                # style=Pack(padding=(0, 5), width=0.5, alignment='center')
            ),
            style=Pack(direction=COLUMN, padding=10)
        )

        # name_label = toga.Label(
        #     "Name : ",
        #     style=Pack(padding=(0, 5), width=0.5, alignment='center')
        # )
        # self.name_input = toga.TextInput(style=Pack(flex=1))

        # income_label = toga.Label(
        #     "Yearly Income : ",
        #     style=Pack(padding=(0, 5), width=0.5, alignment='center')
        # )
        # self.income_input = toga.TextInput(style=Pack(flex=1))

        # company_label = toga.Label(
        #     "Company : ",
        #     style=Pack(padding=(0, 5), width=0.5, alignment='center')
        # )

        submit_button = create_submit_button("Submit", self.submit_info)

        box.add(top_box)
        box.add(submit_button)
        box.add(back_button)
        box.add(bottom_right_box)
        self.add(box)
    
    def submit_info(self, widget):
        self.main_window.info_dialog(
            "TEST",
            "Welcome to Expense Tracking",
        )

class SettingsPage(toga.Box):
    def __init__(self, switch_to_main):
        super().__init__()

        self.label = toga.Label("Settings Screen")
        self.add(self.label)

        self.switch_to_main = switch_to_main

        back_button = toga.Button(
            'Back',
            on_press=self.switch_to_main,
            style=Pack(padding=5)
        )
        self.add(back_button)