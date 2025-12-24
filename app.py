from components.main_window import initial_main_window

class Window():
    def __init__(self, gv):
        self.root = initial_main_window(gv)


class GlobalVar():
    """
    store global variables. eg: the state of a button
    """

    def __init__(self):
        self.var = {}


    def set_value(self, key, value):
        """
        saving variable
        """
        self.var[key] = value

    def get_value(self, key):
        """
        getting variable
        """
        try:
            return self.var[key].get()
        except KeyError:
            return None


if __name__ == "__main__":
    gv = GlobalVar()
    app = Window(gv)
    # app = tb.Window(themename='sandstone')
    app.root.mainloop()
