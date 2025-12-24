# tkinter doesn't provide with tabs, using ttk.notebook instead
from components.widgets import initial_notebook, initial_frame
from tkinter import BOTH

# split into four regions using frames
from components.tab_data_prepare.label_frame_fft_control import initial_label_frame_fft_control
from components.tab_data_prepare.label_frame_sensor_information import initial_label_frame_sensor_information
from components.tab_data_prepare.label_frame_data_process import initial_label_frame_data_process
from components.tab_data_prepare.label_frame_data_visualization import initial_label_frame_data_visualization

from components.tab_summary.label_frame_overview import initial_label_frame_overview
from components.tab_summary.label_frame_banner import initial_label_frame_banner
from components.tab_summary.label_frame_input_parameters import initial_label_frame_input_parameters
from components.tab_summary.label_frame_output_parameters import initial_label_frame_output_parameters


def initial_tabs(parent, gv):
    tab_parent = initial_notebook(parent)
    tab_parent.pack(padx=5,pady=5)
    tab_parent.pack(expand=1, fill=BOTH)

    tab_data_prepare = initial_frame(tab_parent)
    tab_summary = initial_frame(tab_parent)
    tab_parent.add(tab_data_prepare, text='Data Preparation')
    tab_parent.add(tab_summary, text='Summary')

    # first page
    '''initial_label_frame_fft_control(tab_data_prepare, gv)'''
    initial_label_frame_sensor_information(tab_data_prepare, gv)
    initial_label_frame_data_process(tab_data_prepare, gv)
    initial_label_frame_data_visualization(tab_data_prepare, gv)

    # summary page
    #initial_label_frame_overview(tab_summary, gv)
    initial_label_frame_banner(tab_summary, gv)
    initial_label_frame_input_parameters(tab_summary, gv)
    initial_label_frame_output_parameters(tab_summary, gv)

    # history data page
    # initial_label_frame_overview(tab_summary, gv)
    '''initial_label_frame_banner(tab_summary, gv)
    initial_label_frame_input_parameters(tab_summary, gv)
    initial_label_frame_output_parameters(tab_summary, gv)'''

    #tab_history_data = initial_frame(tab_parent)
    #tab_parent.add(tab_history_data, text='Output')
