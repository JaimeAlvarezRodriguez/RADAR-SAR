"""
Proyect:        RADAR SAR
Author:         Jaime Alvarez Rodriguez
Description:    User interface to control and processing signals from RADAR SAR to computer 
"""
import tkinter
import tkinter.messagebox as message
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk
from AppRadar.menu import Menu
from AppRadar.conection_esp32 import WND_Radar_conection, RadarSAR
from AppRadar.plot import matplot_widget, AnalysisWindow
from AppRadar.file_management import load_RADARSAR
from AppRadar.realtime_scope import RealtimeScope
from AppRadar.record import RecordWindow
from AppRadar.analysis import (doppler, ranging, SAR_imaging)

class AppRadar(tkinter.Tk):
    def __init__(self, tittle, geometry):
        super().__init__()
        self.title(tittle)
        self.geometry(geometry)
        #icon = tkinter.PhotoImage(file=, format=".ico")
        #self.iconphoto(True, icon)
        self.iconbitmap(bitmap="./AppRadar/icons/radar.ico")
        self.config(menu=Menu(
            menulist = (
                ("Archivo", 
                    (("Abrir", None, self.open)             ,
                     ("Grabar señal", None, self.record)    ,
                     ("Salir", None, self.destroy)
                    ), 
                ),
                ("Analisis", 
                    (("Señal en tiempo real", None, self.realtime)      ,  
                     ("Velocidad", None, self.doppler)                  ,
                     ("Distancia", None, self.ranging)                  ,
                     ("Imagen SAR", None, self.sar_imaging)
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
        self.matplot.set_labels("Tiempo (s)", "Señal de receptor")
    def place_widgets(self):
        self.matplot.pack()
    def open(self, event=None):
        self.file_route = filedialog.askopenfilename()
        if len(self.file_route) > 0:
            if self.file_route.endswith(".RADARSAR"):
                (data, samplerate) = load_RADARSAR(self.file_route)
                self.matplot.plot(data[1], data[0], samplerate)
                self.matplot.set_title(self.file_route[self.file_route.rindex("/")+1:])
            else:
                message.showwarning("Error de Archivo", "Selecciona un archivo con la extension .RADARSAR")
                self.matplot.set_title("Extensión no compatible")
        else:
            message.showwarning("Error de Archivo", "No seleccionaste ningun archivo")
            self.matplot.set_title("Selecciona un archivo")
        print(self.file_route)
    def record(self, event=None):
        RecordWindow(self, "Grabar .RADARSAR", "400x200", self.radar)
    def realtime(self, event=None):
        RealtimeScope(self, "Señal de receptor", "600x400", self.radar)
    def doppler(self, event=None):
        AnalysisWindow(master=self, 
                       tittle="Velocidad vs tiempo", 
                       file=self.file_route, 
                       progressbar=None, 
                       callback=doppler, 
                       xlabel="Tiempo (s)", 
                       ylabel="Velocidad (km/h)",
                       zmin=-35,
                       zmax=0)
    def ranging(self, event=None):
        AnalysisWindow(master=self, 
                       tittle="Distancia vs tiempo", 
                       file=self.file_route, 
                       progressbar=None, 
                       callback=ranging, 
                       xlabel="Tiempo (s)", 
                       ylabel="Distancia (m)",
                       zmin=-40,
                       zmax=0)
    def sar_imaging(self, event=None):
        AnalysisWindow(master=self, 
                       tittle="Imagen SAR", 
                       file=self.file_route, 
                       progressbar=print, 
                       callback=SAR_imaging, 
                       xlabel="Crossrange (m)", 
                       ylabel="Downrange (m)",
                       zmin=-140,
                       zmax=-80)
    def conexion_esp32(self, event=None):
        WND_Radar_conection(self, "Conectar ESP32", "400x200", self.radar)
    def destroy(self) -> None:
        self.quit()
        return super().destroy()

root = AppRadar(tittle="RADAR SAR", geometry="800x600")
tkinter.mainloop()

