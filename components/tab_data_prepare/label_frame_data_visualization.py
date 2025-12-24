from components.widgets import *
from tkinter import *
from tkinter import ttk
from components.canvas import initial_canvas
import os
from functions.parsing import offset_math


def initial_label_frame_data_visualization(parent, gv):
    label_frame_data_visualization = initial_label_frame(parent, "Data Visualization")
    label_frame_data_visualization.configure(width=150, font=("Sitka Heading", 12, "bold"))
    label_frame_data_visualization.pack(side=RIGHT, fill=BOTH, expand=1)
    label_frame_data_visualization.grid_propagate(0)
    label_frame_data_visualization.pack_propagate(0)

    frame_bottom = initial_frame(label_frame_data_visualization)
    frame_bottom.grid_propagate(0)
    frame_bottom.pack_propagate(0)
    frame_bottom.configure(height=40)
    frame_bottom.pack(side=BOTTOM, fill=X, expand=0, padx=5, pady=5, ipadx=1, ipady=1)
    fill_frame_bottom(frame_bottom, gv)

    frame_top = initial_frame(label_frame_data_visualization)
    frame_top.grid_propagate(0)
    frame_top.pack_propagate(0)
    frame_top.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=3, ipadx=1, ipady=1)
    initial_canvas(frame_top)


def fill_frame_bottom(parent, gv):
    '''checkbutton_c1_dir = initial_checkbutton(parent, "CHANNEL1")
    gv.set_value("checkbutton_c1_dir", IntVar())
    checkbutton_c1_dir.configure(width=10, variable=gv.var["checkbutton_c1_dir"],
                                 command=lambda: channel_dir_selection(gv, 0))  # index starts from 0
    checkbutton_c1_dir.select()
    checkbutton_c1_dir.grid(row=0, column=0, padx=4, pady=4, sticky=NSEW)

    checkbutton_c2_dir = initial_checkbutton(parent, "CHANNEL2")
    gv.set_value("checkbutton_c2_dir", IntVar())
    checkbutton_c2_dir.configure(width=10, variable=gv.var["checkbutton_c2_dir"],
                                 command=lambda: channel_dir_selection(gv,1))
    checkbutton_c2_dir.select()
    checkbutton_c2_dir.grid(row=1, column=0, padx=4, pady=4, sticky=NSEW)

    options = ["channel1", "channel2", "channel3", "channel4", "channel5", "channel6",
               "channel7", "channel8"]
    combobox_window = initial_combobox(parent, options)
    combobox_window.configure(width=11)
    combobox_window.current(0)
    combobox_window.grid(row=1, column=0, padx=4, pady=4, sticky=NSEW)
    img_channel_select = initial_image(filename=r".\.\icons\expand_more.png")
    button_channel_plot_select = initial_button(parent, "Channel Plot")
    button_channel_plot_select.configure(command=lambda: channel_plot_display(gv),
                                         image=img_channel_select, compound=RIGHT)
    button_channel_plot_select.image = img_channel_select
    button_channel_plot_select.grid(column=0, columnspan=2, rowspan=2,
                                    padx=4, pady=4, sticky=NSEW)

    checkbutton_c3_dir = initial_checkbutton(parent, "CHANNEL3")
    gv.set_value("checkbutton_c3_dir", IntVar())
    checkbutton_c3_dir.configure(width=10, variable=gv.var["checkbutton_c3_dir"],
                                 command=lambda: channel_dir_selection(gv, 2))
    checkbutton_c3_dir.select()
    checkbutton_c3_dir.grid(row=0, column=1, padx=4, pady=4, sticky=NSEW)

    checkbutton_c4_dir = initial_checkbutton(parent, "CHANNEL4")
    gv.set_value("checkbutton_c4_dir", IntVar())
    checkbutton_c4_dir.configure(width=10, variable=gv.var["checkbutton_c4_dir"],
                                 command=lambda: channel_dir_selection(gv,3))
    checkbutton_c4_dir.select()
    checkbutton_c4_dir.grid(row=1, column=1, padx=4, pady=4, sticky=NSEW)

    checkbutton_c5_dir = initial_checkbutton(parent, "CHANNEL5")
    gv.set_value("checkbutton_c5_dir", IntVar())
    checkbutton_c5_dir.configure(width=10, variable=gv.var["checkbutton_c5_dir"],
                                 command=lambda: channel_dir_selection(gv, 4))
    checkbutton_c5_dir.select()
    checkbutton_c5_dir.grid(row=0, column=2, padx=4, pady=4, sticky=NSEW)

    checkbutton_c6_dir = initial_checkbutton(parent, "CHANNEL6")
    gv.set_value("checkbutton_c6_dir", IntVar())
    checkbutton_c6_dir.configure(width=10, variable=gv.var["checkbutton_c6_dir"],
                                 command=lambda: channel_dir_selection(gv,5))
    checkbutton_c6_dir.select()
    checkbutton_c6_dir.grid(row=1, column=2, padx=4, pady=4, sticky=NSEW)

    checkbutton_c7_dir = initial_checkbutton(parent, "CHANNEL7")
    gv.set_value("checkbutton_c7_dir", IntVar())
    checkbutton_c7_dir.configure(width=10, variable=gv.var["checkbutton_c7_dir"],
                                 command=lambda: channel_dir_selection(gv, 6))
    checkbutton_c7_dir.select()
    checkbutton_c7_dir.grid(row=0, column=3, padx=4, pady=4, sticky=NSEW)

    checkbutton_c8_dir = initial_checkbutton(parent, "CHANNEL8")
    gv.set_value("checkbutton_c8_dir", IntVar())
    checkbutton_c8_dir.configure(width=10, variable=gv.var["checkbutton_c8_dir"],
                                 command=lambda: channel_dir_selection(gv,7))
    checkbutton_c8_dir.select()
    checkbutton_c8_dir.grid(row=1, column=3, padx=4, pady=4, sticky=NSEW)

    #ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=4, rowspan=2, padx=8, pady=4, sticky=N + S)

    checkbutton_data_offset = initial_checkbutton(parent, "Offset")
    gv.set_value("checkbutton_data_offset", IntVar())
    checkbutton_data_offset.configure(width=7, variable=gv.var["checkbutton_data_offset"])
    checkbutton_data_offset.select()
    checkbutton_data_offset.grid(row=0, column=5, padx=4, pady=4, sticky=NSEW)
    label_data_offset = initial_label(parent, "Offset")
    label_data_offset.configure(width=6)
    label_data_offset.grid(row=0, column=5, padx=4, pady=4, sticky=NSEW)
    entry_data_offset = initial_entry(parent)
    gv.set_value("entry_data_offset", DoubleVar())
    entry_data_offset.configure(width=3, text=gv.var["entry_data_offset"])
    gv.var["entry_data_offset"].set(1)
    entry_data_offset.grid(row=1, column=5, padx=4, pady=4, sticky=NSEW)
    button_offset = initial_button(parent, "Yes")
    button_offset.configure(width=3)
    button_offset.grid(row=1, column=6, padx=4, pady=4, sticky=NSEW)'''

    img_offset = initial_image(filename=r".\.\icons\settinglines.png")
    button_offset = initial_button(parent, " Offset")
    button_offset.configure(width=120, image=img_offset, compound=LEFT, command=offset)
    button_offset.image = img_offset
    button_offset.grid(row=0, column=8, columnspan=2, pady=6)

    """ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=7, rowspan=2, padx=8, pady=4, sticky=N + S)

    checkbutton_data_scale = initial_checkbutton(parent, "Scale")
    gv.set_value("checkbutton_data_scale", IntVar())
    checkbutton_data_scale.configure(width=7, variable=gv.var["checkbutton_data_scale"])
    checkbutton_data_scale.select()
    checkbutton_data_scale.grid(row=0, column=7, padx=4, pady=4, sticky=NSEW)
    label_data_scale = initial_label(parent, "Scale")
    label_data_scale.configure(width=10)
    label_data_scale.grid(row=0, column=8, padx=4, pady=4, sticky=NSEW)
    entry_data_scale = initial_entry(parent)
    gv.set_value("entry_data_scale", DoubleVar())
    entry_data_scale.configure(width=10, text=gv.var["entry_data_scale"])
    gv.var["entry_data_scale"].set(1)
    entry_data_scale.grid(row=1, column=8, padx=4, pady=4, sticky=NSEW)

    #ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=5, rowspan=2, padx=8, pady=4, sticky=N + S)

    label_data_linewidth = initial_label(parent, "Line Width")
    label_data_linewidth.configure(width=10)
    label_data_linewidth.grid(row=0, column=6, padx=4, pady=4, sticky=NSEW)
    entry_data_linewidth = initial_entry(parent)
    gv.set_value("entry_data_linewidth", DoubleVar())
    entry_data_linewidth.configure(width=10, text=gv.var["entry_data_linewidth"])
    gv.var["entry_data_linewidth"].set(1)
    entry_data_linewidth.grid(row=1, column=6, padx=4, pady=4, sticky=NSEW)

    ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=6, rowspan=2, padx=8, pady=4, sticky=N + S)

    checkbutton_fft_cum = initial_checkbutton(parent, "Cumulative")
    gv.set_value("checkbutton_fft_cum", IntVar())
    checkbutton_fft_cum.configure(width=11, variable=gv.var["checkbutton_fft_cum"])
    checkbutton_fft_cum.deselect()
    checkbutton_fft_cum.grid(row=0, column=7, padx=4, pady=4, sticky=NSEW)"""

    """checkbutton_fft_norm = initial_checkbutton(parent, "Normalization")
    gv.set_value("checkbutton_fft_norm", IntVar())
    checkbutton_fft_norm.configure(width=11, variable=gv.var["checkbutton_fft_norm"])
    checkbutton_fft_norm.deselect()
    checkbutton_fft_norm.grid(row=1, column=7, padx=4, pady=4, sticky=NSEW)"""

    """button_fft_plot = initial_button(parent, "FFT Plot")
    button_fft_plot.configure(width=14)
    button_fft_plot.grid(row=0, column=7, padx=4, pady=4, sticky=NSEW)

    button_timehis_plot = initial_button(parent, "Time History Plot")
    button_timehis_plot.configure(width=14)
    button_timehis_plot.grid(row=1, column=7, padx=4, pady=4, sticky=NSEW)"""

    ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=10, rowspan=2, padx=8, pady=4, sticky=N + S)

    img_save = initial_image(filename=r".\.\icons\hard_drive.png")
    button_save = initial_button(parent, " Save")
    button_save.configure(width=100, command=load_data, image=img_save, compound=LEFT)
    button_save.image = img_save
    button_save.grid(row=0, column=11, rowspan=2, padx=4, pady=4, sticky=NSEW)

    ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=12, rowspan=2, padx=8, pady=4, sticky=N + S)

    img_report = initial_image(filename=r".\.\icons\normalization.png")
    button_report = initial_button(parent, "Report")
    button_report.configure(width=100, image=img_report, compound=LEFT)
    button_report.image = img_report
    button_report.grid(row=0, column=13, rowspan=2, padx=4, pady=4, sticky=NSEW)


def load_data():
    # messagebox.showinfo('loading', 'Pass')
    os.startfile(os.getcwd())
    # with open("accounts.pickle", "rb") as f:
    # return None

def offset():
    offset_window = Toplevel()
    offset_window.geometry("300x200")
    offset_window.title("Offset")

    options = ['channel1', 'channel2', 'channel3', 'channel4',
               'channel5', 'channel6', 'channel7', 'channel8']
    combobox_window = initial_combobox(offset_window, options)
    combobox_window.configure(width=8)
    combobox_window.current(0)
    combobox_window.grid(row=1, column=2, padx=4, pady=4)

    entry_offset = initial_entry(offset_window)
    entry_offset.insert(0, '0')
    entry_offset.configure(width=8, relief='sunken')
    entry_offset.grid(row=1, column=4, padx=4, pady=4)

    '''label_offset_tip = initial_label(offset_window, "-1000 ~ 1000")
    label_offset_tip.configure(width=10, font=("Helvetica", 9, "normal"))
    label_offset_tip.grid(row=3, column=4, padx=4, pady=4)'''

    button_offset_sure = initial_button(offset_window, "OK")
    button_offset_sure.configure(width=8, command=lambda: offset_math(combobox_window.get))
    button_offset_sure.grid(row=3, column=2, padx=4, pady=4)