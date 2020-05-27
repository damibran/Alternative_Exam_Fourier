import math
import sys  # We need sys so that we can pass argv to QApplication
import time

from PyQt5 import QtWidgets, QtCore, uic

import pyqtgraph

from program import Signal


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        fileh = QtCore.QFile('GUI.ui')
        fileh.open(QtCore.QFile.ReadOnly)
        uic.loadUi(fileh, self)
        fileh.close()
        # ----------------------------------

        start_time = time.time()
        print("Computing...")
        signal = Signal("Music.wav")
        print("Done in %s seconds" % (time.time() - start_time))

        self.signalGraph.setXRange(0, signal.count_of_samples_per_frame, padding=0)
        self.signalGraph.setYRange(-20000, 20000, padding=0)

        self.spectreGraph.setYRange(0, 200, padding=0)

        self.slider.setMaximum(len(signal.getSignal()[0]) - 1)
        self.slider.setMinimum(0)
        self.slider.valueChanged.connect(self.position_changed(signal))

    def position_changed(self, signal):
        def plot():

            self.signalGraph.clear()
            x = range(0, signal.count_of_samples_per_frame)
            y = signal.getSignal()[0][self.slider.value()]
            self.signalGraph.plot(x, y)

            self.spectreGraph.clear()

            x = []
            for i in range(0, 734):  # signal.count_of_samples_per_frame // 2
                x.append(i * signal.sample_rate / signal.count_of_samples_per_frame)

            s1 = [32.7, 34.65, 36.71, 38.89, 41.2, 43.65, 46.25, 49, 51.91, 55, 58.27, 61.74]
            s2 = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
            notes = {}
            for i in range(1, 8):
                if i:
                    for j in range(0, 12):
                        notes[s1[j]] = str(i) + s2[j]
                        s1[j] = s1[j] * 2

            # freq = x[signal.maximum_freq_on_frame[0][self.slider.value()]]
            keys = list(notes.keys())
            freq = notes[keys[signal.maximum_freq_on_frame[0][self.slider.value()]]]
            self.max_on_frame.setText(str(freq))

            for i in range(1, 734):
                x[i] = math.log10(x[i])

            y = []
            for i in range(0, 734):
                try:
                    y.append(20 * math.log10(signal.getSpectre()[0][self.slider.value()][i]))
                except:
                    y.append(0)

            self.spectreGraph.plot(x, y)
            self.cur_frame.setText(str(self.slider.value()))

        return plot


def getNote(freq):
    s1 = [32.7, 34.65, 36.71, 38.89, 41.2, 43.65, 46.25, 49, 51.91, 55, 58.27, 61.74]
    s2 = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
    notes = {}
    for i in range(1, 8):
        if i:
            for j in range(0, 12):
                notes[s1[j]] = str(i) + s2[j]
                s1[j] = s1[j] * 2

    return notes[asd(freq, notes)]


def asd(x, a):
    b = []
    for i in a:
        b.append(i)
    l = 0
    r = len(b) - 1
    while r - l > 1:
        i = l + (r - l) // 2
        if b[i] > x:
            r = i
        else:
            l = i
    if x - b[l] < b[r] - x:
        return (b[l])
    return (b[r])


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
