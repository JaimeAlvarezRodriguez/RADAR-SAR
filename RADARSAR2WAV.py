import matplotlib.pyplot as plt
import numpy as np
from AppRadar.file_management import load_RADARSAR
from AppRadar.file_management import FILE_EXTENSION


input = "C:/Users/Jaime/Desktop/Grabacion_radar/Distancia/m.RADARSAR"
output = input[:input.rindex(".")] + ".wav"

print(output)

data, samplerate = load_RADARSAR(input)
data[1] = data[1] / 2
data = data.astype(np.int16)

print(data, np.shape(data), type(data[0][0]))

width, heigth = np.shape(data)

#buffer = [(data[i%2][i%heigth]).tobytes() for i in range(width * heigth)]
buffer = data.tobytes()


for i in range(10):
    print(hex(buffer[i]))

print()
print(len(buffer))

plt.plot(data[1])
plt.plot(data[0])
plt.show()