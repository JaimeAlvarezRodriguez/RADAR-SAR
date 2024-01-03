import tkinter.ttk as ttk
import threading
from .new_window import New_window
from .file_management import raw_2_numpy_RADARSAR
from .plot import matplot_widget
from .conection_esp32 import RadarSAR, RAW_DATA_SIZE, DEFAULT_SAMPLERATE

class RealtimeScope(New_window):
    def __init__(self, master, title, geometry, radar = RadarSAR):
        super().__init__(master, title, geometry)
        self.radar = radar
        self.in_progress = False
        self.thr = threading.Thread(target=self.get_data)
        self.create_widgets()
        self.place_widgets()
    def create_widgets(self):
        self.btn_start = ttk.Button(master=self, text="Iniciar", command=self.start)
        self.btn_stop = ttk.Button(master=self, text="Detener", command=self.stop)
        self.matplot = matplot_widget(self)
        self.matplot.set_title("Presiona el boton iniciar")
        self.matplot.set_lim(0, 0.2, -35000, 35000)
    def place_widgets(self):
        self.btn_start.pack()
        self.btn_stop.pack()
        self.matplot.pack()
    def start(self):
        if not self.in_progress and not self.thr.is_alive():
            self.in_progress = True
            self.matplot.set_title("Recibiendo señal...")
            self.thr = threading.Thread(target=self.get_data)
            self.thr.start()
    def stop(self):
        self.in_progress = False
        self.matplot.set_title("Presiona el boton iniciar")
    def get_data(self):
        self.radar.start_record()
        while self.in_progress:
            data = self.radar.get_raw_stream()
            if (len(data) == RAW_DATA_SIZE):
                data = raw_2_numpy_RADARSAR(data)
                self.matplot.plot(data[0], data[1], DEFAULT_SAMPLERATE)
        self.radar.stop_record()
    def destroy(self) -> None:
        if self.in_progress:
            self.stop()
        return super().destroy()
