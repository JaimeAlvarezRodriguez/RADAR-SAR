"""
Proyect:        RADAR SAR
Author:         Jaime Alvarez Rodriguez
Description:    User interface to control and processing signals from RADAR SAR to computer 
"""
import sys
import tkinter
import tkinter.ttk as ttk
import tkinter.messagebox as message
import tkinter.filedialog as filedialog
import tkinter.ttk as ttk
import time
import os
import webbrowser
from AppRadar.menu import Menu
from AppRadar.conection_esp32 import WND_Radar_conection, RadarSAR, get_list_port
from AppRadar.plot import matplot_widget, AnalysisWindow
from AppRadar.file_management import load_RADARSAR
from AppRadar.realtime_scope import RealtimeScope
from AppRadar.record import RecordWindow
from AppRadar.analysis import (doppler, ranging, SAR_imaging)



inner_path = os.path.dirname(__file__)
print("path: ", inner_path)

class AppRadar(tkinter.Tk):
    def __init__(self, tittle, geometry):
        super().__init__()
        self.title(tittle)
        self.geometry(geometry)
        icon = inner_path + "/AppRadar/icons/radar.ico"
        print(icon)
        self.iconbitmap(bitmap=icon, default=icon)
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
                    (("Repositorio", None, self.repository)            ,
                     ("Licencia", None, self.license)               ,
                     ("Guia de uso", None, self.guia)
                    ), 
                )
            ))
        )
        self.file_route = ""
        self.radar = RadarSAR()
        list_port = get_list_port()
        list_port.sort()
        self.radar.port = list_port[0]
        self.radar.timeout = 5

        self.create_widgets()
        self.place_widgets()
        if len(sys.argv) == 2:
            self.open_file(sys.argv[1])
    def create_widgets(self):
        self.matplot = matplot_widget(self)
        self.matplot.plot([0, 0], [0, 0], 10800)
        self.matplot.set_lim(0, 30, -35000, 35000)
        self.matplot.set_labels("Tiempo (s)", "Señal de receptor")
        self.lbl_state = ttk.Label(self, text="")
        self.progressbar = ttk.Progressbar(self, maximum=100, orient="horizontal", mode="determinate")
    def place_widgets(self):
        self.matplot.pack()
    def start_progressbar(self, analisys = str):
        self.lbl_state.pack()
        self.progressbar.pack()
        self.lbl_state["text"] = "Procesando: " + analisys
        self.progressbar["value"] = 0
    def update_progressbar(self, value = int):
        self.progressbar["value"] = value
        print(value)
    def stop_progressbar(self):
        self.lbl_state.forget()
        self.progressbar.forget()
    def verifi_esp32(self):
        self.radar.try_connect()
        return self.radar.status == 1
    def open(self, event=None):
        self.open_file(filedialog.askopenfilename())
    def open_file(self, file = str):
        file = file.replace("\\", "/")
        self.file_route = file
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
        if not self.verifi_esp32():
            message.showwarning("ESP32 no conectado", "Primero conecte el ESP32 desde la pestaña opciones en \"Conectar esp32\"")
            return
        RecordWindow(self, "Grabar .RADARSAR", "400x200", self.radar)
    def realtime(self, event=None):
        RealtimeScope(self, "Señal de receptor", "600x400", self.radar)
    def doppler(self, event=None):
        AnalysisWindow(master=self, 
                       tittle="Velocidad vs tiempo", 
                       file=self.file_route, 
                       progressbar=print, 
                       callback=doppler, 
                       xlabel="Tiempo (s)", 
                       ylabel="Velocidad (km/h)",
                       zmin=-60,
                       zmax=0)
    def ranging(self, event=None):
        AnalysisWindow(master=self, 
                       tittle="Distancia vs tiempo", 
                       file=self.file_route, 
                       progressbar=print, 
                       callback=ranging, 
                       xlabel="Tiempo (s)", 
                       ylabel="Distancia (m)",
                       zmin=-80,
                       zmax=0)
    def sar_imaging(self, event=None):
        AnalysisWindow(master=self, 
                       tittle="Imagen SAR", 
                       file=self.file_route, 
                       progressbar=print, 
                       callback=SAR_imaging, 
                       xlabel="Crossrange (m)", 
                       ylabel="Downrange (m)",
                       zmin=-100,
                       zmax=-40)
    def conexion_esp32(self, event=None):
        WND_Radar_conection(self, "Conectar ESP32", "400x200", self.radar)
    def repository(self, event=None):
        webbrowser.open("https://github.com/JaimeAlvarezRodriguez/RADAR-SAR")
    def license(self, event=None):
        message.showinfo("Licencia", message="Programado con Python 3\n\nBasado en el proyecto \"Build a small radar system\" del MIT\n\nModulos usados:\n-tkinter\n-matplotlib\n-numpy\n-pyserial")
    def guia(self, event=None):
        message.showinfo("Guia de uso", 
        "1.-Enciende el RADAR\n2.-Coloca el RADAR el en modo requerido\n3.-Haz una grabación del RADAR\n4.-Procesa el archivo en su respectivo tipo de análisis\nPara mas información, consultar el manual de usuario del RADAR")
    def destroy(self) -> None:
        self.quit()
        return super().destroy()
    

root = AppRadar(tittle="RADAR SAR", geometry="800x600")
tkinter.mainloop()

