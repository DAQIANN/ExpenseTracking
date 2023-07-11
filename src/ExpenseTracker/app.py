"""
Allowing for tracking of expenses
"""
import toga
import json
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os

from ExpenseTracker.json_backend import load_json, save_json_file
from ExpenseTracker.pages import HomePage, ViewPage

from ExpenseTracker.common import create_submit_button

from ExpenseTracker.constants import FILE_CONSTANTS

initial_user_json = {
    "name" : "",
    "yearly_income" : "",
    "company" : "",
}

def greeting(name, income="", company=""):
        if name:
            initial_user_json["name"] = name
            initial_user_json["yearly_income"] = income
            initial_user_json["company"] = company
            save_json_file(FILE_CONSTANTS["User"], initial_user_json)
            return f"Saved the following information : {name}, {income}, {company}."
        else:
            return "Please input a Name"

class ExpenseTrackerQian(toga.App):

    def startup(self):
        self.main_box = self.make_main_box()
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.continue_screen = HomePage(self.switch_to_main, self.main_window)
        self.data_screen = ViewPage(self.switch_to_main, self.main_window)
        self.main_window.show()
    
    def make_main_box(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        main_box.add(toga.Label('Expense Tracking', style=Pack(font_size=20, text_align='left')))

        info_box = toga.Box(style=Pack(direction=ROW, padding=5))
        button = create_submit_button("Submit", self.submit_info)

        next_button = toga.Button(
            "Next"
        )

        if os.path.exists(FILE_CONSTANTS["User"]):
            current_user = load_json(FILE_CONSTANTS["User"])
            name_label = toga.Label(
                "Hello " + current_user["name"] + "!",
                style=Pack(padding=(0, 5), width=0.5, alignment='left')
            )
            info_box.add(name_label)
        else:
            main_label = toga.Label(
                "Please input some basic data below : ",
                style=Pack(padding=(0, 5), width=0.5, alignment='left')
            )

            name_label = toga.Label(
                "Name : ",
                style=Pack(padding=(0, 5), width=0.5, alignment='left')
            )
            self.name_input = toga.TextInput(style=Pack(flex=1))

            income_label = toga.Label(
                "Yearly Income : ",
                style=Pack(padding=(0, 5), width=0.5, alignment='left')
            )
            self.income_input = toga.TextInput(style=Pack(flex=1))

            company_label = toga.Label(
                "Company : ",
                style=Pack(padding=(0, 5), width=0.5, alignment='left')
            )
            self.company_input = toga.TextInput(style=Pack(flex=1))

            info_box.add(name_label)
            info_box.add(self.name_input)
            info_box.add(income_label)
            info_box.add(self.income_input)
            info_box.add(company_label)
            info_box.add(self.company_input)
            info_box.add(button)

        switch_to_continue_button = toga.Button(
            "Input Expenses",
            on_press=self.switch_to_continue,
            style=Pack(padding=5, width=150)
        )

        switch_to_data_button = toga.Button(
            "View Expenses",
            on_press=self.switch_to_data,
            style=Pack(padding=5, width=150)
        )

        main_box.add(info_box)
        main_box.add(switch_to_continue_button)
        main_box.add(switch_to_data_button)
        main_box.style.update(alignment='left')
        return main_box

    def submit_info(self, widget):
        self.main_window.info_dialog(
            greeting(self.name_input.value, self.income_input.value, self.company_input.value),
            "Welcome to Expense Tracking",
        )
    
    def switch_to_continue(self, widget):
        self.main_window.content = self.continue_screen
    
    def switch_to_data(self, widget):
        self.main_window.content = self.data_screen
    
    def switch_to_main(self, widget):
        self.main_window.content = self.main_box

def main():
    return ExpenseTrackerQian()
