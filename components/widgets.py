# control the widget properties from tkinter
import tkinter.font as tkFont
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


font_family = "Lucida Sans"

font_size = {
    "small": 9,
    "normal": 10,
    "large": 11,
    "Large": 12
}

text_color = "#000000"

background_color = "#f5f7fa"


def initial_entry(parent):
    font_style = tkFont.Font(family=font_family, size=font_size["normal"], weight="normal")
    return Entry(parent, bg="#eef0f4", disabledbackground=background_color,
                 fg=text_color, font=font_style)


def initial_menu(parent):
    font_style = tkFont.Font(family=font_family, size=font_size["large"], weight="normal")
    return Menu(parent, bg="#f5f7fa", fg=text_color, font=font_style, tearoff=False)


def initial_notebook(parent):
    """style = ttk.Style(parent)
    style.theme_use("default")
    style.configure('TNotebook.Tab', background="e4e6eb")"""
    notebook = ttk.Notebook(parent)
    #return ttk.Notebook(parent)
    return notebook


def initial_frame(parent, custom_name=None):
    # frame = Frame(parent, bg = "#121212", relief = "raised")
    frame = Frame(parent, bg="#f5f7fa", relief="raised", name=custom_name)
    return frame


def initial_label_frame(parent, label):
    font_style = tkFont.Font(family=font_family, size=font_size["large"], weight="normal")
    label_frame = LabelFrame(parent, text=label, bg="#f5f7fa", fg=text_color, font=font_style,
                             relief="groove", borderwidth=1, padx=15, pady=10)
    return label_frame


def initial_treeview(parent, show):
    treeview = ttk.Treeview(parent, show=show)
    return treeview


def initial_label(parent, label):
    font_style = tkFont.Font(family=font_family, size=font_size["normal"], weight="normal")
    # label = Label(parent,text=label,bg="#3B3B3B", fg = text_color, font = font_style)
    label = Label(parent, text=label, bg="#f5f5f5", fg=text_color, font=font_style)

    return label


def initial_button(parent, label):
    font_style = tkFont.Font(family=font_family, size=font_size["normal"], weight="normal")
    button = Button(parent, bg="#eef0f4", fg=text_color, text=label,font=font_style, relief="groove",)
    return button


def initial_checkbutton(parent, label):
    font_style = tkFont.Font(family=font_family, size=font_size["normal"], weight="normal")
    checkbutton = Checkbutton(parent, bg="#f5f5f5", fg=text_color, text=label,
                              font=font_style, relief="groove")
    #checkbutton = ttk.Checkbutton(parent, text=label,variable=1)
    return checkbutton


def initial_combobox(parent, options):
    font_style = tkFont.Font(family=font_family, size=font_size["normal"], weight="normal")
    combobox = ttk.Combobox(parent, value=options, font=font_style, state="readonly")
    return combobox


def initial_image(filename):
    myimg = ImageTk.PhotoImage(Image.open(filename).resize((30, 30)))
    return myimg
