import tkinter
from .import debug

if debug:
    import sys
    print(sys.argv)
    import os
    print(os.getcwd())

class New_window(tkinter.Toplevel):
    def __init__(self, master, tittle, geometry):
        super().__init__(master=master)
        self.title(tittle)
        self.geometry(geometry)
    def create_widgets(self):
        pass
    def place_widgets(self):
        pass

    
