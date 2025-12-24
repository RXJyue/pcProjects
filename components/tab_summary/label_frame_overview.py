# from ..widgets import initial_label_frame, initial_treeview
from components.widgets import initial_label_frame, initial_treeview
from tkinter import *


def initial_label_frame_overview(parent, gv):
    label_frame_model_information = initial_label_frame(parent, "Model Information")
    label_frame_model_information.configure(width=150)
    label_frame_model_information.pack(side=LEFT, fill=Y, expand=0)
    label_frame_model_information.grid_propagate(1)
    label_frame_model_information.pack_propagate(1)
    treeview_model_information = initial_treeview(label_frame_model_information, "tree")
    treeview_model_information.pack(side=LEFT, fill=Y, expand=0)
    treenode_sensor_number = treeview_model_information.insert("", '0', "appVersion", text="App Version")
    treenode_sensor_coordinate = treeview_model_information.insert("", '1', "modelID", text="Model")
    treenode_sensor_number = treeview_model_information.insert("", '0', "CRC", text="CRC")
