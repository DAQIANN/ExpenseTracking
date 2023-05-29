import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.constants import CENTER
import os
from datetime import date

from ExpenseTracker.json_backend import load_json, save_json_file
from ExpenseTracker.common import create_submit_button

user_entry = {
    "Cost" : "",
    "Type" : "",
    "Date" : ""
}

class HomePage(toga.Box):
    def __init__(self, switch_to_main, main_window):
        super().__init__()

        self.switch_to_main = switch_to_main
        self.main_window = main_window

        box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        box.add(toga.Label('Start tracking your expenses!', style=Pack(font_size=20, text_align='center')))

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

        year_selection = toga.Selection(items=[str(year) for year in range(2000, 2051)], style=Pack(flex=1))
        year_selection.on_select = self.on_date_selected

        month_selection = toga.Selection(items=['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'], style=Pack(flex=1))
        month_selection.on_select = self.on_date_selected

        day_selection = toga.Selection(items=[str(day) for day in range(1, 32)], style=Pack(flex=1))
        day_selection.on_select = self.on_date_selected

        box.add(top_box)
        box.add(year_selection)
        box.add(month_selection)
        box.add(day_selection)
        box.add(submit_button)
        box.add(back_button)
        box.add(bottom_right_box)
        self.add(box)
    
    def submit_info(self, widget):
        self.main_window.info_dialog(
            "TEST",
            "Welcome to Expense Tracking",
        )
    
    def on_date_selected(self, widget):
        date = widget.value
        print("Selected date: ", type(date), date)

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