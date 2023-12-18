"""
Proyect:        RADAR SAR
Author:         Jaime Alvarez Rodriguez
Description:    User interface to control and processing signals from RADAR SAR to computer 
"""
import tkinter
import tkinter.messagebox as message
import tkinter.filedialog as filedialog
from AppRadar.menu import Menu
from AppRadar.conection_esp32 import WND_Radar_conection, RadarSAR
from AppRadar.plot import matplot_widget
from AppRadar.file_management import load_RADARSAR
from AppRadar.realtime_scope import RealtimeScope
from AppRadar.record import RecordWindow

class AppRadar(tkinter.Tk):
    def __init__(self, tittle, geometry):
        super().__init__()
        self.title(tittle)
        self.geometry(geometry)
        self.config(menu=Menu(
            menulist = (
                ("Archivo", 
                    (("Abrir", None, self.open)          ,
                     ("Grabar señal", None, self.record)   ,
                     ("Salir", None, self.destroy)
                    ), 
                ),
                ("Analisis", 
                    (("Señal en tiempo real", None, self.realtime)   ,  
                     ("Velocidad", None, None)              ,
                     ("Distancia", None, None)              ,
                     ("Imagen SAR", None, None)
                    ), 
                ),
                ("Opciones", 
                    (("Conexion esp32", None, self.conexion_esp32)         , 
                    ), 
                ),
                ("Ayuda", 
                    (("Repositorio", None, None)            ,
                     ("Licencia", None, None)               ,
                    ), 
                )
            ))
        )
        self.file_route = ""
        self.radar = RadarSAR()
        self.radar.timeout = 5

        self.create_widgets()
        self.place_widgets()
    def create_widgets(self):
        self.matplot = matplot_widget(self)
        self.matplot.plot([0, 0], [0, 0], 10800)
        self.matplot.set_lim(0, 0.8, -35000, 35000)
    def place_widgets(self):
        self.matplot.pack()
    def open(self, event=None):
        file = filedialog.askopenfilename()
        if len(file) > 0:
            if file.endswith(".RADARSAR"):
                self.file_route = file
                (data, samplerate) = load_RADARSAR(self.file_route)
                self.matplot.plot(data[1], data[0], samplerate)
            else:
                message.showwarning("Error de Archivo", "Selecciona un archivo con la extension .RADARSAR")
        else:
            message.showwarning("Error de Archivo", "No seleccionaste ningun archivo")
        print(self.file_route)
    def record(self, event=None):
        RecordWindow(self, "Grabar .RADARSAR", "400x200", self.radar)
    def realtime(self, event=None):
        RealtimeScope(self, "Señal de receptor", "600x400", self.radar)
    def conexion_esp32(self, event=None):
        WND_Radar_conection(self, "Conectar ESP32", "400x200", self.radar)
    def destroy(self) -> None:
        self.quit()
        return super().destroy()

root = AppRadar(tittle="RADAR SAR", geometry="800x600")
tkinter.mainloop()

