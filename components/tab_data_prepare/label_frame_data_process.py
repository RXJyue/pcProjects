from tkinter import filedialog
from components.widgets import *
from functions.channel_selection import channel_dir_selection
from functions.parsing import load_data, offset_math


def initial_label_frame_data_process(parent, gv):
    label_frame_data_process = initial_label_frame(parent, "Data Process")
    label_frame_data_process.configure(width=150, font=("Sitka Heading", 12, "bold"))
    label_frame_data_process.pack(side=LEFT, fill=Y, expand=0, padx=10)
    # label_frame_data_process.grid(row=0, column=1)
    label_frame_data_process.grid_propagate(1)
    label_frame_data_process.pack_propagate(1)
    fill_label_frame_data_process(label_frame_data_process, gv)


def fill_label_frame_data_process(parent, gv):
    # img_sheets = ImageTk.PhotoImage(file=r".\.\icons\app1.png")
    # href = "https://www.flaticon.com/free-icons/file-upload"
    img_sheets = initial_image(filename=r".\.\icons\upload-file.png")
    button_load_data = initial_button(parent, " Load")
    button_load_data.configure(width=120, command=load_data, image=img_sheets, compound=LEFT)
    button_load_data.image = img_sheets  # reference such that image won't disappear
    button_load_data.grid(row=0, columnspan=2, padx=3, pady=3)

    """button_struct_prop = initial_button(parent, "Struct. Prop.")
    button_struct_prop.configure(width=13)
    button_struct_prop.grid(row=1, columnspan=2, padx=3, pady=3)"""

    # ttk.Separator(parent, orient=HORIZONTAL).grid(row=2, columnspan=2, pady=3, sticky=W + E)

    """checkbutton_x_select = initial_checkbutton(parent, "X direction")
    gv.set_value("checkbutton_x_select", IntVar())
    checkbutton_x_select.configure(width=11, variable=gv.var["checkbutton_x_select"],borderwidth=0,
                                   command=lambda: update_dir_select_message(gv, 0),
                                   state=DISABLED)
    checkbutton_x_select.select()
    checkbutton_x_select.grid(row=3, columnspan=2, padx=3, pady=3)

    checkbutton_y_select = initial_checkbutton(parent, "Y direction")
    gv.set_value("checkbutton_y_select", IntVar())
    checkbutton_y_select.configure(width=11, variable=gv.var["checkbutton_y_select"],borderwidth=0,
                                   command=lambda: update_dir_select_message(gv, 1),
                                   state=DISABLED)
    checkbutton_y_select.select()
    checkbutton_y_select.grid(row=4, columnspan=2, padx=3, pady=3)

    checkbutton_z_select = initial_checkbutton(parent, "Z direction")
    gv.set_value("checkbutton_z_select", IntVar())
    checkbutton_z_select.configure(width=11, variable=gv.var["checkbutton_z_select"],borderwidth=0,
                                   command=lambda: update_dir_select_message(gv, 2))
    checkbutton_z_select.select()
    checkbutton_z_select.grid(row=5, columnspan=2, padx=3, pady=3)"""

    ttk.Separator(parent, orient=HORIZONTAL).grid(row=6, columnspan=2, pady=3, sticky=W + E)

    checkbutton_demean = initial_checkbutton(parent, "Demean")
    gv.set_value("checkbutton_demean", IntVar())
    checkbutton_demean.configure(width=11, variable=gv.var["checkbutton_demean"])
    checkbutton_demean.select()
    checkbutton_demean.grid(row=7, columnspan=2, padx=3, pady=3)

    ttk.Separator(parent, orient=HORIZONTAL).grid(row=8, columnspan=2, pady=3, sticky=W + E)

    checkbutton_filter = initial_checkbutton(parent, "Filter")
    gv.set_value("checkbutton_filter", IntVar())
    checkbutton_filter.configure(width=11, variable=gv.var["checkbutton_filter"])
    checkbutton_filter.select()
    checkbutton_filter.grid(row=9, columnspan=2, padx=3, pady=3)

    options = ["Lowpass", "Highpass", "Bandpass", "Bandstop"]
    combobox_filter = initial_combobox(parent, options)
    combobox_filter.configure(width=11)
    combobox_filter.current(0)
    combobox_filter.grid(row=10, columnspan=2, padx=3, pady=3)

    label_low_filter = initial_label(parent, "Low (Hz)")
    label_low_filter.configure(width=7)
    label_low_filter.grid(row=11, column=0, padx=3, pady=3)
    entry_low_filter = initial_entry(parent)
    gv.set_value("entry_low_filter", DoubleVar())
    entry_low_filter.configure(width=6, text=gv.var["entry_low_filter"],
                               state='disabled')
    gv.var["entry_low_filter"].set(0)
    entry_low_filter.grid(row=11, column=1, padx=3, pady=3, sticky=N + S)

    label_high_filter = initial_label(parent, "High (Hz)")
    label_high_filter.configure(width=7)
    label_high_filter.grid(row=12, column=0, padx=1, pady=3)
    entry_high_filter = initial_entry(parent)
    gv.set_value("entry_high_filter", DoubleVar())
    entry_high_filter.configure(width=6, text=gv.var["entry_high_filter"],
                                state='disabled')
    gv.var["entry_high_filter"].set(0)
    entry_high_filter.grid(row=12, column=1, padx=1, pady=3, sticky=N + S)

    label_filter_order = initial_label(parent, "Order")
    label_filter_order.configure(width=7)
    label_filter_order.grid(row=13, column=0, pady=3)
    entry_filter_order = initial_entry(parent)
    gv.set_value("entry_filter_order", IntVar())
    entry_filter_order.configure(width=6, text=gv.var["entry_filter_order"],
                                 state='disabled')
    gv.var["entry_filter_order"].set(2)
    entry_filter_order.grid(row=13, column=1, pady=3, sticky=N + S)

    ttk.Separator(parent, orient=HORIZONTAL).grid(row=14, columnspan=2, pady=3, sticky=W + E)

    checkbutton_window = initial_checkbutton(parent, "Window")
    gv.set_value("checkbutton_window", IntVar())
    checkbutton_window.configure(width=11, variable=gv.var["checkbutton_window"])
    gv.var["checkbutton_window"].set(1)
    checkbutton_window.grid(row=15, columnspan=2, pady=3)

    options = ["Hanning", "Bartlett", "Hamming", "Blackman-Harris", "Parzen", "Taylor", "Tukey", "Kaiser", "Chebyshev",
               "Gaussian", "Rectangluar"]
    combobox_window = initial_combobox(parent, options)
    combobox_window.configure(width=11)
    combobox_window.current(0)
    combobox_window.grid(row=16, columnspan=2, pady=3)

    label_win_param = initial_label(parent, "Parm.")
    label_win_param.configure(width=7)
    label_win_param.grid(row=17, column=0, pady=3)
    entry_win_param = initial_entry(parent)
    gv.set_value("entry_win_param", DoubleVar())
    entry_win_param.configure(width=6, text=gv.var["entry_win_param"],
                              state='disabled')
    gv.var["entry_win_param"].set(0)
    entry_win_param.grid(row=17, column=1, pady=3, sticky=N + S)

    ttk.Separator(parent, orient=HORIZONTAL).grid(row=18, columnspan=2, pady=3, sticky=W + E)

    img_channel_select = initial_image(filename=r".\.\icons\expand_more.png")
    button_channel_plot_select = initial_button(parent, "Channel Plot")
    button_channel_plot_select.configure(width=120, command=lambda: channel_plot_display(gv),
                                         image=img_channel_select, compound=RIGHT)
    button_channel_plot_select.image = img_channel_select
    button_channel_plot_select.grid(row=19, columnspan=2, pady=6)

    '''img_run = initial_image(filename=r".\.\icons\startup.png")
    button_run = initial_button(parent, " Run")
    button_run.configure(width=100, command=load_data, image=img_run, compound=LEFT)
    button_run.image = img_run
    button_run.grid(row=19, columnspan=2, pady=6)
    

    img_plot = initial_image(filename=r".\.\icons\ssid_chart.png")
    button_plot = initial_button(parent, " Plot")
    button_plot.configure(width=100, command=load_data, image=img_plot, compound=LEFT)
    button_plot.image = img_plot
    button_plot.grid(row=20, columnspan=2, pady=3)'''

    img_fft = initial_image(filename=r".\.\icons\transformation.png")
    button_fft = initial_button(parent, " FFT")
    button_fft.configure(width=120, command=fft_control, image=img_fft, compound=LEFT)
    button_fft.image = img_fft
    button_fft.grid(row=21, columnspan=2, pady=6)


def channel_plot_display(gv):
    channels = Toplevel()
    channels.geometry("300x200")
    channels.title("Channel Selection")

    for i in range(1, 9):
        checkbutton_dir = initial_checkbutton(channels, "channel" + str(i))
        gv.set_value("checkbutton_c" + str(i) + "_dir", IntVar())
        checkbutton_dir.configure(width=10, variable=gv.var["checkbutton_c" + str(i) + "_dir"],
                                  command=lambda: channel_dir_selection(gv, 3))
        checkbutton_dir.select()
        checkbutton_dir.grid(row=int((i + i % 2) / 2), column=(i % 2 + 1) % 2, padx=4, pady=4, sticky=NSEW)

    button_sure = initial_button(channels, "OK")
    button_sure.configure(width=7, font=('arial', '11', 'bold'), command=channels.destroy)
    button_sure.grid(padx=4, pady=4, sticky=NSEW)


def fft_control():
    fft_values = Toplevel()
    fft_values.geometry("400x300")
    fft_values.title("FFT control")

    label_low_crop = initial_label(fft_values, "Low (Hz)")
    label_low_crop.configure(width=10)
    label_low_crop.grid(row=1, column=1, padx=3, pady=3)
    entry_low_crop = initial_entry(fft_values)
    entry_low_crop.insert(0, '0.5')
    entry_low_crop.configure(width=7, relief='flat', state='disable')
    entry_low_crop.grid(row=1, column=2, pady=15)

    ttk.Separator(fft_values, orient=HORIZONTAL).grid(row=2, columnspan=10, pady=3, sticky=W + E)

    label_high_crop = initial_label(fft_values, "High (Hz)")
    label_high_crop.configure(width=10)
    label_high_crop.grid(row=3, column=1, padx=3, pady=3)
    entry_high_crop = initial_entry(fft_values)
    entry_high_crop.insert(0, '0.5')
    entry_high_crop.configure(width=7, relief='flat', state='disable')
    entry_high_crop.grid(row=3, column=2, padx=3, pady=3)
    # fft_values = ["Low (Hz): 0.5","High (Hz): 0.5","FFT Power: 18","window Power: 1","Resolution: 0"]
    # messagebox.showinfo("FFT control",'\n'.join(fft_values))



