from components.widgets import *
from tkinter import *
from tkinter import ttk


def initial_label_frame_output_parameters(parent, gv):
    label_frame_output_parameters = initial_label_frame(parent, "OUTPUT")

    label_frame_output_parameters.configure(height=400)
    label_frame_output_parameters.pack(ipadx=10, ipady=10, expand=True, side=LEFT, fill=BOTH)
    label_frame_output_parameters.grid_propagate(1)
    label_frame_output_parameters.pack_propagate(1)

    frame_RMS_output_voltage = initial_frame(label_frame_output_parameters, custom_name="output voltage")
    frame_RMS_output_voltage.grid_propagate(0)
    frame_RMS_output_voltage.pack_propagate(0)
    frame_RMS_output_voltage.configure(height=70,background='white')
    frame_RMS_output_voltage.pack(side=TOP, fill=X, expand=0,
                                 padx=5, pady=5, ipadx=1, ipady=1)
    fill_frame_parameters(frame_RMS_output_voltage, gv)

    frame_RMS_output_current = initial_frame(label_frame_output_parameters, custom_name="output current")
    frame_RMS_output_current.grid_propagate(0)
    frame_RMS_output_current.pack_propagate(0)
    frame_RMS_output_current.configure(height=70, background='white')
    frame_RMS_output_current.pack(side=TOP, fill=X, expand=0,
                                 padx=5, pady=5, ipadx=1, ipady=1)
    fill_frame_parameters(frame_RMS_output_current, gv)

    frame_RMS_output_frequency = initial_frame(label_frame_output_parameters, custom_name="output frequency")
    frame_RMS_output_frequency.grid_propagate(0)
    frame_RMS_output_frequency.pack_propagate(0)
    frame_RMS_output_frequency.configure(height=70, background='white')
    frame_RMS_output_frequency.pack(side=TOP, fill=X, expand=0,
                                 padx=5, pady=5, ipadx=1, ipady=1)
    fill_frame_parameters(frame_RMS_output_frequency, gv)


def fill_frame_parameters(parent, gv):

    label_RMS_output_voltage = initial_label(parent, label=str(parent._name))
    label_RMS_output_voltage.configure(width=40,background='white')
    label_RMS_output_voltage.grid(row=1, column=0, padx=3, pady=4)

    label_RMS_output_voltage_value = initial_label(parent, "NA")
    label_RMS_output_voltage_value.configure(width=40, background='white',
                                            font=('Helvetica 15 bold'))
    label_RMS_output_voltage_value.grid(row=2, column=0, padx=3, pady=3)

