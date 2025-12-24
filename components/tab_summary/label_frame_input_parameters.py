from components.widgets import *
from tkinter import *


def initial_label_frame_input_parameters(parent, gv):
    label_frame_input_parameters = initial_label_frame(parent, "INPUT")

    label_frame_input_parameters.configure(height=400)
    label_frame_input_parameters.pack(ipadx=10, ipady=10, expand=True, side=LEFT, fill=BOTH)
    label_frame_input_parameters.grid_propagate(1)
    label_frame_input_parameters.pack_propagate(1)

    frame_RMS_input_voltage = initial_frame(label_frame_input_parameters, custom_name="input voltage")
    frame_RMS_input_voltage.grid_propagate(0)
    frame_RMS_input_voltage.pack_propagate(0)
    frame_RMS_input_voltage.configure(height=70,background='white')
    frame_RMS_input_voltage.pack(side=TOP, fill=X, expand=0,
                                 padx=5, pady=5, ipadx=1, ipady=1)
    fill_frame_parameters(frame_RMS_input_voltage, gv)

    frame_RMS_input_current = initial_frame(label_frame_input_parameters, custom_name="input current")
    frame_RMS_input_current.grid_propagate(0)
    frame_RMS_input_current.pack_propagate(0)
    frame_RMS_input_current.configure(height=70, background='white')
    frame_RMS_input_current.pack(side=TOP, fill=X, expand=0,
                                 padx=5, pady=5, ipadx=1, ipady=1)
    fill_frame_parameters(frame_RMS_input_current, gv)

    frame_RMS_input_frequency = initial_frame(label_frame_input_parameters, custom_name="input frequency")
    frame_RMS_input_frequency.grid_propagate(0)
    frame_RMS_input_frequency.pack_propagate(0)
    frame_RMS_input_frequency.configure(height=70, background='white')
    frame_RMS_input_frequency.pack(side=TOP, fill=X, expand=0,
                                 padx=5, pady=5, ipadx=1, ipady=1)
    fill_frame_parameters(frame_RMS_input_frequency, gv)


def fill_frame_parameters(parent, gv):

    label_RMS_input_voltage = initial_label(parent, label=str(parent._name))
    label_RMS_input_voltage.configure(width=40,background='white')
    label_RMS_input_voltage.grid(row=1, column=0, padx=3, pady=4)

    label_RMS_input_voltage_value = initial_label(parent, "NA")
    label_RMS_input_voltage_value.configure(width=40, background='white',
                                            font=('Helvetica 15 bold'))
    label_RMS_input_voltage_value.grid(row=2, column=0, padx=3, pady=3)

    """label_RMS_input_current = initial_label(parent, "RMS Input Current(AC)")
    label_RMS_input_current.configure(width=20)
    label_RMS_input_current.grid(row=2, column=0, padx=3, pady=3)

    label_RMS_input_current_value = initial_label(parent, "7.2A")
    label_RMS_input_current_value.configure(width=20,font=('Helvetica 16 bold'))
    label_RMS_input_current_value.grid(row=3, column=0, padx=3, pady=3)"""

