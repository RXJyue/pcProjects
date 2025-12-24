import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import BOTH
from functions.parsing import load_data

"""def random_numbers():
    np.random.seed(0)

    freq = 1 # 频率=50HZ
    amp = 1 # 幅值
    time = np.arange(0,2,0.001) #采样时间为1s, 频率为1000HZ
    sine_wave = amp * np.sin(2*np.pi*freq*time)

    c1_list = np.random.rand(2000)
    #c1_list = np.random.rand(2000) * np.sin(2*np.pi*freq*time)
    c2_list = np.random.rand(2000)+5
    c3_list = np.random.rand(2000)+10

    nat_list = range(0, 2000)

    return c1_list, c2_list, c3_list, nat_list"""


def initial_canvas(parent):
    # c1_list, c2_list, c3_list, nat_list = random_numbers()
    input_file = load_data()
    input_file_dict = input_file.to_dict('list')

    time = input_file_dict['time']
    '''c1_list = input_file_dict['c1_list']
    c2_list = input_file_dict['c2_list']
    c3_list = input_file_dict['c3_list']
    c4_list = input_file_dict['c4_list']
    c5_list = input_file_dict['c5_list']
    c6_list = input_file_dict['c6_list']
    c7_list = input_file_dict['c7_list']
    c8_list = input_file_dict['c8_list']'''
    channel1 = input_file_dict['channel1']
    channel2 = input_file_dict['channel2']
    channel3 = input_file_dict['channel3']
    channel4 = input_file_dict['channel4']
    channel5 = input_file_dict['channel5']
    channel6 = input_file_dict['channel6']
    channel7 = input_file_dict['channel7']
    channel8 = input_file_dict['channel8']

    plt.ion()
    figure = Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.grid(True)
    ax.set_xlabel("Time (unit)")
    ax.set_ylabel("Parameters")
    figure.subplots_adjust(top=0.95)

    '''channels_list = ['c1_list', 'c2_list', 'c3_list', 'c4_list',
                     'c5_list', 'c6_list', 'c7_list', 'c8_list']
    for channel in channels_list:
        channel = input_file[channel]
        ax.plot(time, channel)
    legend2 = figure.legend(['channel1', 'channel2', 'channel3', 'channel4',
                             'channel5', 'channel6', 'channel7', 'channel8'],
                            loc='outside right upper')'''

    # 循环迭代无法适配offset
    channels_list = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8']
    c1, = ax.plot(time, channel1, label='channel1')
    c2, = ax.plot(time, channel2, label='channel2')
    c3, = ax.plot(time, channel3, label='channel3')
    c4, = ax.plot(time, channel4, label='channel4')
    c5, = ax.plot(time, channel5, label='channel5')
    c6, = ax.plot(time, channel6, label='channel6')
    c7, = ax.plot(time, channel7, label='channel7')
    c8, = ax.plot(time, channel8, label='channel8')
    ax.autoscale_view()
    # c1,c2,c3, = ax.plot(time,c1_list,time,c2_list,time,c3_list)
    channel_legend = figure.legend(loc='outside right upper')
    ax.add_artist(channel_legend)

    canvas = FigureCanvasTkAgg(figure, parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)

    # initiate toolbar object and bind to canvas
    toolbar = NavigationToolbar2Tk(canvas, parent)
    toolbar.update()
    # toolbar.configure(background="#f5f7fa")
    canvas.get_tk_widget().pack(fill=BOTH, expand=1)
