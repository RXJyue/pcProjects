from components.widgets import *
from tkinter import *
from PIL import Image, ImageTk


def initial_label_frame_banner(parent, gv):
    label_frame_overview = initial_label_frame(parent, "Info")
    # img_carrier = initial_image(filename=r".\.\icons\normalization.png")

    # label_frame_overview.grid_propagate(0) #frame大小不可变，grid-行和列
    # label_frame_overview.pack_propagate(0) #frame大小不可变，pack-盒子&组件

    label_frame_overview.configure(height=90)
    label_frame_overview.pack(ipadx=50, ipady=50, fill=BOTH)
    # label_frame_overview.image = img_carrier
    label_frame_overview.grid_propagate(0)
    label_frame_overview.pack_propagate(0)
    fill_frame_overview(label_frame_overview, gv)


def fill_frame_overview(parent, gv):
    #img_carrier = initial_image(filename=r".\.\icons\carrier_logo_r.png")
    img_carrier = ImageTk.PhotoImage(Image.open(r".\.\icons\carrier_logo_r.png").resize((125,50)))

    label_banner_title = initial_label(parent, "        INTERNAL TEST USE")
    label_banner_title.configure(width=400, height=100, font=('Microsoft YaHei', '12', 'bold'),
                     image=img_carrier,compound=LEFT,background='#f5f7fa')
    label_banner_title.image=img_carrier
    #label_banner_title.pack()
    label_banner_title.grid(row=0, column=1)
    #label1.place(relx = 0.5, rely = 0.5,anchor='center')

    ttk.Separator(parent, orient=VERTICAL).grid(row=0, column=2, rowspan=2, padx=15, sticky=N + S)

    status_column = ['Name', '222222']
    treeview_status = initial_treeview(parent,'tree')
    treeview_status['columns'] = ('1','2')
    treeview_status.column("1", anchor='c')
    treeview_status.column("2", anchor='c')
    treeview_status.heading("1", text="id")
    treeview_status.heading("2", text="Name")
    treeview_status.pack(fill=Y, expand=0)

    treenode_serial_number = treeview_status.insert("",2, "serialNum", text="Serial Number",
                                                    values=1)

