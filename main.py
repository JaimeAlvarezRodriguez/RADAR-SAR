"""
Proyect:        RADAR SAR
Author:         Jaime Alvarez Rodriguez
Description:    User interface to control and processing signals from RADAR SAR to computer 
"""
import tkinter
from AppRadar.new_window import New_window

class AppRadar(tkinter.Tk):
    def __init__(self, tittle, geometry):
        super().__init__()
        self.title(tittle)
        self.geometry(geometry)

root = AppRadar(tittle="RADAR SAR", geometry="600x400")
tkinter.mainloop()

