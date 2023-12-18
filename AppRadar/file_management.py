"""
File management for extension .RADARSAR

using little endian system

Structure
1-4 :   Data size of samples
5-8 :   Sample rate
9-10:   Signal
    1-12:   receptor signal
    13-15:  None
    16:     Pulse sync
Repeat bytes 9-10
"""

import numpy as np

FILE_EXTENSION = ".RADARSAR"
DEFAULT_NAME = "radar" + FILE_EXTENSION

def load_raw_RADARSAR(file=DEFAULT_NAME):
    file = open(file, mode="rb")
    number_samples = int.from_bytes(file.read(4), byteorder="little")
    samplerate = int.from_bytes(file.read(4), byteorder="little")
    data = file.read(number_samples)
    file.close()
    return (data, samplerate)

def save_raw_RADARSAR(file=DEFAULT_NAME, samplerate = int, data = bytes):
    file = open(file, mode="wb")
    file.write(len(data).to_bytes(4, byteorder="little"))
    file.write(samplerate.to_bytes(4, byteorder="little"))
    file.write(data)
    file.close()
    
def numpy_2_raw_RADARSAR(data):
    print(data, np.shape(data))

def raw_2_numpy_RADARSAR(data_raw = bytes):
    data = np.frombuffer(data_raw, dtype=np.uint8)
    data = np.reshape(data, newshape=(len(data)//2, 2)).astype(np.uint16)
    data_byte = data[:, 0] + (data[:, 1] << 8)
    data[:, 0] = data_byte & 0x7fff
    data[:, 1] = (data_byte >> 15)
    data = data.T.astype(float)
    data[0] = (data[0] - 1680) * (1 << 4)
    data[1] = data[1] * 0xffff - 0x7fff
    return data

def load_RADARSAR(file = DEFAULT_NAME):
    (data, samplerate) = load_raw_RADARSAR(file)
    data = raw_2_numpy_RADARSAR(data)
    return (data, samplerate)

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    (data, samplerate) = load_raw_RADARSAR("C:/Users/Jaime/Desktop/Grabacion_radar/caminando.RADARSAR")
    print(samplerate)
    print(len(data))
    data = raw_2_numpy_RADARSAR(data)
    num = np.linspace(0, len(data[0]) / samplerate, len(data[0]))
    plt.ylim([-35000, 35000])
    plt.plot(num, data[1])
    plt.plot(num, data[0])
    plt.show()