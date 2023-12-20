import tkinter
import numpy as np
import gc
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from .new_window import New_window

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
    def set_labels(self, xlabel, ylabel):
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.canvas.draw()

class AnalysisWindow(New_window):
    def __init__(self, master, tittle, file, progressbar, callback, xlabel, ylabel, zmin, zmax):
        super().__init__(master, tittle, "600x400")
        (self.x, self.y, self.z) = callback(file, progressbar)
        gc.collect()
        self.file = file
        self.create_widgets()
        self.place_widgets()
        self.create_pcolormesh(zmin, zmax, xlabel, ylabel, "Potencia antena receptora (dB)")
    def create_widgets(self):
        self.matplot = matplot_widget(self)
    def place_widgets(self):
        self.matplot.pack()
    def create_pcolormesh(self, zmin, zmax, xlabel, ylabel, zlabel):
        mpp = self.matplot.ax.pcolormesh(self.x, self.y, self.z, vmin=zmin, vmax=zmax)
        self.matplot.fig.colorbar(mpp, label=zlabel)
        self.matplot.set_title(self.file[self.file.rindex("/")+1:])
        self.matplot.set_labels(xlabel, ylabel)
