# bottom text box message clicking the check buttons of direction selection

def channel_dir_selection(gv, dir):
    channel_Label = ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"][dir]
    var_name = "checkbutton_" + channel_Label + "_dir"
    if gv.var[var_name].get():
        gv.var["message_field"].set("Data in " + channel_Label + " channel is selected.")
    else:
        gv.var["message_field"].set("Data in " + channel_Label + " channel is deselected.")
