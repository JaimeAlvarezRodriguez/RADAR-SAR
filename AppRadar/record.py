import threading
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as message
from .file_management import save_raw_list_RADARSAR, FILE_EXTENSION
from .new_window import New_window
from .conection_esp32 import RadarSAR, RAW_DATA_SIZE, INFO_SMPRTE, DEFAULT_SAMPLERATE

class RecordWindow(New_window):
    def __init__(self, master, tittle, geometry, radar = RadarSAR):
        super().__init__(master, tittle, geometry)
        self.radar = radar
        self.cont = 0
        self.in_progress = False
        self.create_widgets()
        self.place_widgets()
        
    def create_widgets(self):
        self.lbl_status = ttk.Label(self, text="Presiona Start para comenzar")
        self.lbl_cont = ttk.Label(self, text=self.cont_string())
        self.btn_start = ttk.Button(self, text="Start", command=self.start)
        self.btn_stop = ttk.Button(self, text="Guardar", command=self.stop)
    def place_widgets(self):
        self.lbl_status.pack()
        self.lbl_cont.pack()
        self.btn_start.pack()
        self.btn_stop.pack()
    def start(self):
        self.in_progress = True
        self.lbl_status['text'] = "Grabando"
        self.lbl_cont.after(1000, self.f_cont)
        threading.Thread(target=self.record).start()
    def stop(self):
        self.in_progress = False
    def f_cont(self):
        if self.in_progress:
            self.cont = self.cont + 1
            self.lbl_cont["text"] = self.cont_string()
            print(self.cont_string())
            self.after(1000, self.f_cont)
        else:
            self.cont = 0
            self.lbl_cont["text"] = self.cont_string()
    def record(self):
        print("hola")
        data = []
        self.radar.start_record()
        while self.in_progress:
            data.append(self.radar.get_raw_stream())
        self.lbl_status['text'] = "Deteniendo de grabar.."
        self.radar.stop_record()
        self.lbl_status['text'] = "Guardando..."
        file = filedialog.asksaveasfilename(filetypes=(("Archivos de RADAR SAR", "*.RADARSAR"),))
        
        if not (len(file) > 0):
            message.showerror("No se pudo guardar el archivo", "No seleccionaste una ruta de archivo")
            return
        if  not file.endswith(FILE_EXTENSION):
            file = file + FILE_EXTENSION
        try:
            samplerate = round(float(self.radar.request_info(INFO_SMPRTE)))
        except:
            samplerate = DEFAULT_SAMPLERATE
        print(file)
        save_raw_list_RADARSAR(file, samplerate, data, RAW_DATA_SIZE)
        self.lbl_status['text'] = "Presiona Start para comenzar"
    def cont_string(self):
        s = self.cont % 60
        m = (self.cont // 60) % 60
        h = (self.cont // 3600)
        if s < 10:
            s = "0" + str(s)
        if m < 10:
            m = "0" + str(m)
        if h < 10:
            h = "0" + str(h)       
        return str(h) + ":" + str(m) + ":" + str(s)
    