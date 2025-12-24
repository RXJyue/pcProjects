import pandas as pd
from tkinter import filedialog


def load_data():
    file_path = filedialog.askopenfilename()
    input_file = pd.read_excel(file_path)

    return input_file


def offset_math(this_list: list):
    input_file = load_data()
    # input_file_dict = input_file.to_dict()

    number = float(input("offset: "))

    this_list_updated = []
    for x in this_list:
        this_list_updated.append(x + number)

    return this_list_updated
