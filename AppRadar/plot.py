import tkinter
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class matplot_widget:
    def __init__(self, master):
        self.fig = Figure()
        self.ax = self.fig.subplots()
        self.fig.add_axes(self.ax)
        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=master)
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.signal = self.ax.plot([0])[0]
        self.sync = self.ax.plot([0])[0]
        self.canvas.draw()
    def on_key_press(self, event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, self.canvas, self.toolbar)
    def pack(self):
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    def plot(self, signal, sync, samplerate):
        num = np.linspace(0, len(signal) / samplerate, len(signal))
        self.signal.set_xdata(num)
        self.sync.set_xdata(num)
        self.signal.set_ydata(signal)
        self.sync.set_ydata(sync)
        self.canvas.draw()
    def set_lim(self, xmin, xmax, ymin, ymax):
        self.ax.set_ylim(ymin=ymin, ymax=ymax)
        self.ax.set_xlim(xmin=xmin, xmax=xmax)
        self.canvas.draw()
    def set_title(self, title):
        self.ax.set_title(title)
        self.canvas.draw()