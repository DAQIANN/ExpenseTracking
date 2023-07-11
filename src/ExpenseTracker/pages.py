import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from toga.constants import CENTER
import os
from datetime import timedelta, datetime

from ExpenseTracker.json_backend import load_json, save_json_file
from ExpenseTracker.common import create_submit_button
from ExpenseTracker.transaction import Transaction
from ExpenseTracker.constants import FILE_CONSTANTS, MONTHS_CONVERSION

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
            'Back to Main Menu',
            on_press=self.switch_to_main,
            style=Pack(padding=5)
        )

        top_box = toga.Box(
            toga.Label(
                "Please observe the inputs below : ",
            ),
            style=Pack(direction=COLUMN, padding=10)
        )

        cost_label = toga.Label(
            "Cost : ",
            style=Pack(padding=(0, 5), width=100, alignment='center')
        )
        self.cost_input = toga.TextInput(style=Pack(flex=1))

        transaction_label = toga.Label(
            "Transaction Type : ",
            style=Pack(padding=(0, 5), width=0.5, alignment='center')
        )
        transact_selection = toga.Selection(items=['None', 'Travel', 'Online Shopping', 'In-Store Shopping', 'Dining', 'Groceries'], style=Pack(flex=1, padding=5))
        transact_selection.on_select = self.on_transact_selected
        self.transact_type = 'None'

        year_label = toga.Label(
            "Year : ",
            style=Pack(padding=(0, 5), width=0.5, alignment='center')
        )
        year_selection = toga.Selection(items=['None'] + [str(year) for year in range(2000, 2051)], style=Pack(flex=1, padding=5))
        year_selection.on_select = self.on_year_selected
        self.year = 'None'

        month_label = toga.Label(
            "Month : ",
            style=Pack(padding=(0, 5), width=0.5, alignment='center')
        )
        month_selection = toga.Selection(items=['None', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'], style=Pack(flex=1, padding=5))
        month_selection.on_select = self.on_month_selected
        self.month = 'None'
        
        day_label = toga.Label(
            "Day : ",
            style=Pack(padding=(0, 5), width=0.5, alignment='center')
        )
        day_selection = toga.Selection(items=['None'] + [str(day) for day in range(1, 32)], style=Pack(flex=1, padding=5))
        day_selection.on_select = self.on_day_selected
        self.day = 'None'

        submit_button = create_submit_button("Submit", self.submit_info)

        switch_to_continue_button = toga.Button(
            "Continue to View Expenses",
            on_press=self.switch_to_continue,
            style=Pack(padding=5, width=180)
        )
    
        box.add(top_box)
        box.add(cost_label)
        box.add(self.cost_input)
        box.add(transaction_label)
        box.add(transact_selection)
        box.add(year_label)
        box.add(year_selection)
        box.add(month_label)
        box.add(month_selection)
        box.add(day_label)
        box.add(day_selection)
        box.add(submit_button)
        box.add(switch_to_continue_button)
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

            test_document = open(FILE_CONSTANTS["User_Data"])
            if test_document.read().strip() == '':
                transaction_dictionary = {}
                test_document.close()
            else:
                transaction_dictionary = load_json(FILE_CONSTANTS["User_Data"])
            
            if transact_date_key not in transaction_dictionary:
                transaction_dictionary[transact_date_key] = []
            
            transaction_dictionary[transact_date_key].append(transaction)
            save_json_file(FILE_CONSTANTS["User_Data"], transaction_dictionary)
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
    
    def switch_to_continue(self, widget):
        self.view_screen = ViewPage(self.switch_to_main, self.main_window)
        self.main_window.content = self.view_screen

# this page is meant to view transactions from a certain time to another time and organized in the different categories available
class ViewPage(toga.Box):
    def __init__(self, switch_to_main, main_window):
        super().__init__()

        self.box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.box.add(toga.Label('View your Expenses!', style=Pack(font_size=20, text_align='center')))

        self.switch_to_main = switch_to_main
        self.main_window = main_window

        back_button = toga.Button(
            'Back to Main Menu',
            on_press=self.switch_to_main,
            style=Pack(padding=5)
        )

        confirm_button = toga.Button(
            'Confirm',
            on_press=self.on_confirm_click,
            style=Pack(padding=5)
        )

        start_date_label = toga.Label('Select a Start Date : ', style=Pack(flex=1, padding=5))

        start_year_selection = toga.Selection(items=['None'] + [str(year) for year in range(2000, 2030)], style=Pack(flex=1, padding=5))
        start_year_selection.on_select = self.on_start_year_selected
        self.start_year = 'None'

        start_month_selection = toga.Selection(items=['None', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'], style=Pack(flex=1, padding=5))
        start_month_selection.on_select = self.on_start_month_selected
        self.start_month = 'None'

        start_day_selection = toga.Selection(items=['None'] + [str(day) for day in range(1, 32)], style=Pack(flex=1, padding=5))
        start_day_selection.on_select = self.on_start_day_selected
        self.start_day = 'None'

        start_input_box = toga.Box(style=Pack(direction=ROW))
        start_input_box.add(start_year_selection)
        start_input_box.add(start_month_selection)
        start_input_box.add(start_day_selection)

        end_date_label = toga.Label('Select an End Date : ', style=Pack(flex=1, padding=5))

        end_year_selection = toga.Selection(items=['None'] + [str(year) for year in range(2000, 2030)], style=Pack(flex=1, padding=5))
        end_year_selection.on_select = self.on_end_year_selected
        self.end_year = 'None'

        end_month_selection = toga.Selection(items=['None', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'], style=Pack(flex=1, padding=5))
        end_month_selection.on_select = self.on_end_month_selected
        self.end_month = 'None'

        end_day_selection = toga.Selection(items=['None'] + [str(day) for day in range(1, 32)], style=Pack(flex=1, padding=5))
        end_day_selection.on_select = self.on_end_day_selected
        self.end_day = 'None'

        end_input_box = toga.Box(style=Pack(direction=ROW))
        end_input_box.add(end_year_selection)
        end_input_box.add(end_month_selection)
        end_input_box.add(end_day_selection)

        self.box.add(start_date_label)
        self.box.add(start_input_box)
        self.box.add(end_date_label)
        self.box.add(end_input_box)
        self.box.add(confirm_button)
        self.box.add(back_button)
        self.box.style.update(alignment='center')
        self.add(self.box)

    def on_start_year_selected(self, widget):
        self.start_year = widget.value
    
    def on_start_month_selected(self, widget):
        self.start_month = widget.value
    
    def on_start_day_selected(self, widget):
        self.start_day = widget.value

    def on_end_year_selected(self, widget):
        self.end_year = widget.value
    
    def on_end_month_selected(self, widget):
        self.end_month = widget.value
    
    def on_end_day_selected(self, widget):
        self.end_day = widget.value
    
    def on_confirm_click(self, widget):
        if self.start_year == 'None' or self.end_year == 'None' or self.start_month == 'None' or self.end_month == 'None' or self.start_day == 'None' or self.end_day == 'None':
            self.main_window.info_dialog(
                "Error",
                "Can not have None Values. Please input valid dates.",
            )
            return
        elif int(self.start_year) > int(self.end_year):
            self.main_window.info_dialog(
                "Error",
                "The Start Year can not be later than the End Year. Please correct the dates.",
            )
            return
        start = self.start_year + '-' + str(MONTHS_CONVERSION[self.start_month]) + '-' + self.start_day
        end = self.end_year + '-' + str(MONTHS_CONVERSION[self.end_month]) + '-' + self.end_day
        self.stats_screen = StatsPage(self.main_window, self, start, end)
        self.main_window.content = self.stats_screen

class StatsPage(toga.Box):
    def __init__(self, main_window, view_window, start_date, end_date):
        super().__init__()

        self.box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.box.add(toga.Label('View your Expenses!', style=Pack(font_size=20, text_align='center')))

        self.main_window = main_window
        self.view_window = view_window

        back_button = toga.Button(
            'Back',
            on_press=self.switch_to_view,
            style=Pack(padding=5)
        )
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        cost_data = load_json(FILE_CONSTANTS["User_Data"])
        data_type = {"Total" : float(0)}
        for key in cost_data:
            current_date = datetime.strptime(key, "%Y-%m-%d")
            if start <= current_date <= end:
                for i in cost_data[key]:
                    if i.get_transaction_type() not in data_type:
                        data_type[i.get_transaction_type()] = float(0)
                    data_type[i.get_transaction_type()] += i.get_cost()
                    data_type["Total"] += i.get_cost()

        for key in data_type:
            self.box.add(toga.Label(key + " : " + str(round(data_type[key], 2)), style=Pack(font_size=15, text_align='center')))
        self.box.add(back_button)
        self.box.style.update(alignment='center')
        self.add(self.box)

    def switch_to_view(self, widget):
        self.main_window.content = self.view_window