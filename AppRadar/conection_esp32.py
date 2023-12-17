import serial
import serial.tools.list_ports as listport
import tkinter
import tkinter.ttk as tkk
from .new_window import New_window

RQST_NONE__ = 0
RQST_INFO__ = 1
RQST_RECORD = 3

INFO_MACADR = 1
INFO_SMPRTE = 2

RECD_START_ = 1
RECD_STOP__ = 2

MSSG_STOP = "$STOP_RECORDING_ESP32#"

RAW_DATA_SIZE = 10000
DATA_SIZE = 5000

def get_list_port():
    list_port = []
    for port in listport.comports():
        list_port.append(port.name)
        list_port.sort()
    return list_port

class RadarSAR(serial.Serial):
    def __init__(self):
        super().__init__()
    def setPort(self, port):
        self.port = port
    def send_message(self, request = int, value = int):
        request = int(request) & 0xff
        value = int(value) & 0xff
        message = (request << 8) & value
        self.write(message.to_bytes(2))
    def request_info(self, value = int):
        self.send_message(request=RQST_INFO__, value=value)
    def start_record(self):
        self.send_message(request=RQST_RECORD, value=RECD_START_)
    def stop_record(self):
        self.send_message(request=RQST_RECORD, value=RECD_STOP__)
        self.read_until(MSSG_STOP.encode("ascii"))


class WND_Radar_conection(New_window):
    def __init__(self, master, title, geometry):
        super().__init__(master, title, geometry)
        self.radar = RadarSAR()
        self.list_port = get_list_port()
        self.create_widgets()
        self.place_widgets()
    def create_widgets(self):
        self.select_port = tkk.Combobox(master=self.master, state="readonly",
                                        values=self.list_port)
        self.select_port.set(self.list_port[0])
        
    def place_widgets(self):
        self.select_port.pack()