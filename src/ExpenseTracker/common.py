import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.constants import CENTER
import os

from ExpenseTracker.json_backend import load_json, save_json_file

def create_submit_button(label, send_function):
    button = toga.Button(
        label,
        on_press=send_function,
        style=Pack(padding=5, width=100)
    )

    return button

# def create_back_button():