# from .widgets import initial_menu
import os.path

from components.widgets import initial_menu
from tkinter import messagebox
import webbrowser

def initial_menus(parent):
    menubar = initial_menu(parent)
    parent.config(menu=menubar)

    menu_file = initial_menu(menubar)
    menubar.add_cascade(label='File', menu=menu_file)

    # menu_file.add_command(label='New', command=os.startfile(r'C:'))
    #menu_file.add_command(label='Save', accelerator="Ctrl+N", command=save_file)
    menu_file.add_command(label="Exit", accelerator="Alt+Q", command=parent.quit)

    menu_help = initial_menu(menubar)
    menubar.add_cascade(label='Help', menu=menu_help)
    menu_help.add_command(label="README", command=add_info)
    menu_help.add_command(label="More...", command=add_info)


def save_file():
    # open new file
    os.startfile(os.getcwd())
    # parent.event_generate("<Control-Key-n>")


def add_info():
    webbrowser.open(r".\README.md","r")
    #messagebox.showinfo('说明', 'Pass')
