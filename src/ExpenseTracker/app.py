"""
Allowing for tracking of expenses
"""
import toga
import json
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import httpx
import os

from ExpenseTracker.json_backend import load_json, save_json_file
from ExpenseTracker.pages import HomePage, SettingsPage

from ExpenseTracker.common import create_submit_button

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
            save_json_file('/Users/danielqian/Documents/ExpenseTracker/src/ExpenseTracker/data/user.json', initial_user_json)
            return f"Saved the following information : {name}, {income}, {company}."
        else:
            return "Please input a Name"

class ExpenseTrackerQian(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_box = self.make_main_box()
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.continue_screen = HomePage(self.switch_to_main, self.main_window)
        self.settings_screen = SettingsPage(self.switch_to_main)
        self.main_window.show()
    
    def make_main_box(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        main_box.add(toga.Label('Expense Tracking', style=Pack(font_size=20, text_align='center')))

        info_box = toga.Box(style=Pack(direction=ROW, padding=5))
        button = create_submit_button("Submit", self.submit_info)

        next_button = toga.Button(
            "Next"
        )

        if os.path.exists('/Users/danielqian/Documents/ExpenseTracker/src/ExpenseTracker/data/user.json'):
            current_user = load_json('/Users/danielqian/Documents/ExpenseTracker/src/ExpenseTracker/data/user.json')
            name_label = toga.Label(
                "Hello " + current_user["name"] + "!",
                style=Pack(padding=(0, 5), width=0.5, alignment='center')
            )
            info_box.add(name_label)
        else:
            main_label = toga.Label(
                "Please input some basic data below : ",
                style=Pack(padding=(0, 5), width=0.5, alignment='center')
            )

            name_label = toga.Label(
                "Name : ",
                style=Pack(padding=(0, 5), width=0.5, alignment='center')
            )
            self.name_input = toga.TextInput(style=Pack(flex=1))

            income_label = toga.Label(
                "Yearly Income : ",
                style=Pack(padding=(0, 5), width=0.5, alignment='center')
            )
            self.income_input = toga.TextInput(style=Pack(flex=1))

            company_label = toga.Label(
                "Company : ",
                style=Pack(padding=(0, 5), width=0.5, alignment='center')
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
            "Continue",
            on_press=self.switch_to_continue,
            style=Pack(padding=5, width=100)
        )

        switch_to_settings_button = toga.Button(
            "Settings",
            on_press=self.switch_to_settings,
            style=Pack(padding=5, width=100)
        )

        main_box.add(info_box)
        main_box.add(switch_to_continue_button)
        main_box.add(switch_to_settings_button)
        main_box.style.update(alignment='center')
        return main_box

    def submit_info(self, widget):
        # async with httpx.AsyncClient() as client:
        #     response = await client.get("https://jsonplaceholder.typicode.com/posts/42")

        # payload = response.json()

        self.main_window.info_dialog(
            greeting(self.name_input.value, self.income_input.value, self.company_input.value),
            "Welcome to Expense Tracking",
        )
    
    def switch_to_continue(self, widget):
        self.main_window.content = self.continue_screen

    def switch_to_settings(self, widget):
        self.main_window.content = self.settings_screen
    
    def switch_to_main(self, widget):
        self.main_window.content = self.main_box

def main():
    return ExpenseTrackerQian()
