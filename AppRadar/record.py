import tkinter.ttk as ttk
from .new_window import New_window
from .conection_esp32 import RadarSAR

class RecordWindow(New_window):
    def __init__(self, master, tittle, geometry, radar = RadarSAR):
        super().__init__(master, tittle, geometry)
        self.create_widgets()
        self.place_widgets()
        self.radar = radar
    def create_widgets(self):
        self.lbl_status = ttk.Label(self, text="Presiona Start para comenzar")
        self.lbl_cont = ttk.Label(self, text="00:00:00")
        self.btn_start = ttk.Button(self, text="Start")
        self.btn_stop = ttk.Button(self, text="Guardar")
    def place_widgets(self):
        self.lbl_status.pack()
        self.lbl_cont.pack()
        self.btn_start.pack()
        self.btn_stop.pack()