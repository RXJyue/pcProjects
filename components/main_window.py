import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
# from .menus import initial_menus
from components.menus import initial_menus
# from .message_field import initial_message_field
from components.message_field import initial_message_field
# from .tabs import initial_tabs
from components.tabs import initial_tabs
import ctypes


def initial_main_window(gv):
    root = tk.Tk()
    # root.tk.call("lappend", "auto_path", "Azure-ttk-theme-main")
    # root.tk.call("package", "require", "light")

    root.geometry("1100x700")#+2000+100
    root.title("VFD health check & diagnostic tool")
    root.configure(background="#f5f7fa")

    #获取屏幕尺寸并显示在屏幕中央
    '''screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = 1007
    height = 640
    window_size = f'{width}x{height}+{round((screen_width-width)/2)}+{round((screen_height-height)/2)}'
    root.geometry(window_size)'''

    root.style = ttk.Style()
    root.style.theme_use("vista")
    #root.style.configure("Treeview", background="#f5f7fa")
    root.style.configure("TNotebook", background="#f5f7fa", padx=5)
    root.style.configure("TNotebook.Tab", background="#eef0f4")

    root.iconbitmap(default=r".\icons\battery_saver.ico")

    # change default taskbar icon
    myappid = 'car.vhcdt.app1.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # initialize menu bars
    initial_menus(root)

    # initialize message field
    initial_message_field(root, gv)

    # initialize tabs
    initial_tabs(root, gv)

    return root
