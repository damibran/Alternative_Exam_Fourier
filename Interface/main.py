from PyQt5 import QtWidgets,QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import wave
import numpy as np
import math
from program import Signal

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        fileh = QtCore.QFile('GUI.ui')
        fileh.open(QtCore.QFile.ReadOnly)
        uic.loadUi(fileh, self)
        fileh.close()
        #----------------------------------
        
        self.signalGraph.setXRange(0, 8192, padding=0)
        self.signalGraph.setYRange(-20000, 20000, padding=0)

        self.spectreGraph.setYRange(0, 200, padding=0)

        signal=Signal("Test_Chords.wav")

        print(signal.getDuration())

        self.track_duration.setText(str(signal.getDuration()))

        self.slider.setMaximum(len(signal.getSignal()[0])-1)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.position_changed(signal))

    def position_changed(self,signal):
        def plot():

            self.signalGraph.clear()
            x=range(0,8192)
            y=signal.getSignal()[0][self.slider.value()]
            self.signalGraph.plot(x, y)

            self.spectreGraph.clear()
            x=[]
            for i in range(0,4096):
                x.append(i*signal.sample_rate/4096)
            for i in range(1,4096):
                x[i]=math.log10(x[i])
            y=[]
            for i in range(0,4096):
                try:
                    y.append(20*math.log10(signal.getSpectre()[0][self.slider.value()][i]))
                except:
                    y.append(0)
            self.spectreGraph.plot(x, y)
            self.cur_frame.setText(str(self.slider.value()))

        return plot

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
    main()