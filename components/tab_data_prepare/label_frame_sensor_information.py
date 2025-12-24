# from ..widgets import initial_label_frame, initial_treeview
from components.widgets import *
from tkinter import *
from PIL import Image, ImageTk


def initial_label_frame_sensor_information(parent, gv):
    label_frame_sensor_information = initial_label_frame(parent, "Sensor Information")
    label_frame_sensor_information.configure(width=110, font=("Sitka Heading",12,"bold"))
    label_frame_sensor_information.pack(side=TOP, fill=X, expand=0)
    #label_frame_sensor_information.grid(row=0, column=0)
    label_frame_sensor_information.grid_propagate(1)
    label_frame_sensor_information.pack_propagate(1)
    """treeview_sensor_information = initial_treeview(label_frame_sensor_information, "tree")
    treeview_sensor_information.pack(side=LEFT, fill=Y, expand=0)
    treenode_app_version = treeview_sensor_information.insert("", '1', "appVersion", text="App Version")
    treenode_sensor_number = treeview_sensor_information.insert("", '1', "sensorNum", text="Sensor Number")
    treenode_sensor_coordinate = treeview_sensor_information.insert("", '2', "sensorCoord", text="Sensor Coordinate")
    treenode_serial_number = treeview_sensor_information.insert("", '3', "serialNum", text="Serial Number")
    treenode_CRC = treeview_sensor_information.insert("", '4', "CRC", text="CRC")"""

    fill_label_frame_sensor_information(label_frame_sensor_information, gv)


def fill_label_frame_sensor_information(parent, gv):
    img_carrier = ImageTk.PhotoImage(Image.open(r".\.\icons\carrier_logo_r.png").resize((80, 32)))

    label_app_version = initial_label(parent, "      App version")
    label_app_version.configure(width=200, image=img_carrier, compound=LEFT,background='#f5f7fa')
    label_app_version.image=img_carrier
    label_app_version.grid(row=0, column=1)
    entry_app_version = initial_entry(parent)
    gv.set_value("entry_app_version", DoubleVar())
    entry_app_version.configure(width=6, text=gv.var["entry_app_version"],
                                state='disabled', relief='flat')
    gv.var["entry_app_version"].set('v1.0.0')
    entry_app_version.grid(row=0, column=2, sticky=N + S)

    ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=3, rowspan=2, padx=15, sticky=N + S)

    label_model_version = initial_label(parent, "Model version")
    label_model_version.configure(width=12)
    label_model_version.grid(row=0, column=4)
    entry_model_version = initial_entry(parent)
    gv.set_value("entry_model_version", DoubleVar())
    entry_model_version.configure(width=6, text=gv.var["entry_model_version"],
                                state='disabled', relief='flat')
    gv.var["entry_model_version"].set('900A')
    entry_model_version.grid(row=0, column=5, sticky=N + S)

    ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=6, rowspan=2, padx=15, sticky=N + S)

    label_app_CRC = initial_label(parent, "App CRC")
    label_app_CRC.configure(width=12)
    label_app_CRC.grid(row=0, column=7)
    entry_app_CRC = initial_entry(parent)
    gv.set_value("entry_app_CRC", DoubleVar())
    entry_app_CRC.configure(width=8, text=gv.var["entry_app_CRC"],
                                state='disabled', relief='flat')
    gv.var["entry_app_CRC"].set('441B0017')
    entry_app_CRC.grid(row=0, column=8, sticky=N + S)

    ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=9, rowspan=2, padx=15, sticky=N + S)

    label_loader_version = initial_label(parent, "Loader version")
    label_loader_version.configure(width=16)
    label_loader_version.grid(row=0, column=10)
    entry_loader_version = initial_entry(parent)
    gv.set_value("entry_loader_version", DoubleVar())
    entry_loader_version.configure(width=10, text=gv.var["entry_loader_version"],
                            state='disabled', relief='flat')
    gv.var["entry_loader_version"].set('A189271')
    entry_loader_version.grid(row=0, column=11, sticky=N + S)