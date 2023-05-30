import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from toga.constants import CENTER
import os
from datetime import timedelta, datetime

from ExpenseTracker.json_backend import load_json, save_json_file
from ExpenseTracker.common import create_submit_button
from ExpenseTracker.transaction import Transaction

user_entry = {
    "Cost" : "",
    "Type" : "",
}

MONTHS_CONVERSION = {
    'January' : 1,
    'February' : 2,
    'March' : 3,
    'April' : 4,
    'May' : 5,
    'June' : 6,
    'July' : 7,
    'August' : 8,
    'September' : 9,
    'October' : 10,
    'November' : 11,
    'December' : 12,
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

        cost_label = toga.Label(
            "Cost : ",
            style=Pack(padding=(0, 5), width=0.5, alignment='center')
        )
        self.cost_input = toga.TextInput(style=Pack(flex=1))

        transact_selection = toga.Selection(items=['None', 'Travel', 'Online Shopping', 'In-Store Shopping', 'Dining', 'Groceries'], style=Pack(flex=1, padding=5))
        transact_selection.on_select = self.on_transact_selected
        self.transact_type = 'None'

        year_selection = toga.Selection(items=['None'] + [str(year) for year in range(2000, 2051)], style=Pack(flex=1, padding=5))
        year_selection.on_select = self.on_year_selected
        self.year = 'None'

        month_selection = toga.Selection(items=['None', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'], style=Pack(flex=1, padding=5))
        month_selection.on_select = self.on_month_selected
        self.month = 'None'

        day_selection = toga.Selection(items=['None'] + [str(day) for day in range(1, 32)], style=Pack(flex=1, padding=5))
        day_selection.on_select = self.on_day_selected
        self.day = 'None'

        submit_button = create_submit_button("Submit", self.submit_info)

        box.add(top_box)
        box.add(cost_label)
        box.add(self.cost_input)
        box.add(transact_selection)
        box.add(year_selection)
        box.add(month_selection)
        box.add(day_selection)
        box.add(submit_button)
        box.add(back_button)
        box.add(bottom_right_box)
        self.add(box)
    
    def submit_info(self, widget):
        if self.year == 'None' or self.month == 'None' or self.day == 'None':
            self.main_window.info_dialog(
                "Expense Tracker",
                "Please Make a Selection in Every Entry",
            )
        else:
            transact_date = datetime(int(self.year), MONTHS_CONVERSION[self.month], int(self.day))
            transact_date_key = transact_date.strftime('%Y-%m-%d')
            print(transact_date_key)
            transaction = Transaction(self.transact_type, float(self.cost_input.value))

            if open('/Users/danielqian/Documents/ExpenseTracker/src/ExpenseTracker/data/user_data.json').read().strip() == '':
                transaction_dictionary = {}
            else:
                transaction_dictionary = load_json('/Users/danielqian/Documents/ExpenseTracker/src/ExpenseTracker/data/user_data.json')
            
            if transact_date_key not in transaction_dictionary:
                transaction_dictionary[transact_date_key] = []
            
            transaction_dictionary[transact_date_key].append(transaction)
            save_json_file('/Users/danielqian/Documents/ExpenseTracker/src/ExpenseTracker/data/user_data.json', transaction_dictionary)
            self.main_window.info_dialog(
                "Expense Tracker",
                "Your Transaction Information has been Tracked",
            )

    def on_year_selected(self, widget):
        self.year = widget.value

    def on_month_selected(self, widget):
        self.month = widget.value

    def on_day_selected(self, widget):
        self.day = widget.value

    def on_transact_selected(self, widget):
        self.transact_type = widget.value

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