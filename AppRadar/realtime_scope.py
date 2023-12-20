import tkinter.ttk as ttk
from .new_window import New_window
from .file_management import raw_2_numpy_RADARSAR
from .plot import matplot_widget
from .conection_esp32 import RadarSAR, RAW_DATA_SIZE

class RealtimeScope(New_window):
    def __init__(self, master, title, geometry, radar = RadarSAR):
        super().__init__(master, title, geometry)
        self.radar = radar
        self.in_progress = False
        self.create_widgets()
        self.place_widgets()
    def create_widgets(self):
        self.btn_start = ttk.Button(master=self, text="Iniciar", command=self.start)
        self.btn_stop = ttk.Button(master=self, text="Detener", command=self.stop)
        self.matplot = matplot_widget(self)
        self.matplot.set_title("Presiona el boton iniciar")
        self.matplot.set_lim(0, 0.2, -35000, 35000)
        self.btn_start.after(100, self.update_data)
    def place_widgets(self):
        self.btn_start.pack()
        self.btn_stop.pack()
        self.matplot.pack()
    def start(self):
        self.in_progress = True
        self.matplot.set_title("Recibiendo señal...")
        self.radar.start_record()
    def stop(self):
        self.in_progress = False
        self.matplot.set_title("Presiona el boton iniciar")
        self.radar.stop_record()
    def update_data(self):
        if self.radar.status == 1 and self.in_progress:
            data = self.radar.read(RAW_DATA_SIZE)
            print(len(data))
            data = raw_2_numpy_RADARSAR(data)
            self.matplot.plot(data[0], data[1], 11672)
        self.after(10, self.update_data)
    def destroy(self) -> None:
        if self.in_progress:
            self.stop()
        return super().destroy()
