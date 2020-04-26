from PyQt5 import QtWidgets,QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import wave
import numpy as np
import math

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        fileh = QtCore.QFile('GUI.ui')
        fileh.open(QtCore.QFile.ReadOnly)
        uic.loadUi(fileh, self)
        fileh.close()
        #----------------------------------
        
        self.graphWidget.setXRange(0, 8129, padding=0)
        self.graphWidget.setYRange(-20000, 20000, padding=0)

        self.getSignal()

        self.track_duration.setText(str(duration))

        

        self.slider.setMaximum(len(frame[0]))

        self.slider.sliderMoved.connect(self.slide)

        """self.plot(x,y)

    def plot(self, x, y):
        self.graphWidget.plot(x, y)"""

    def slide(self):
        self.graphWidget.clear()
        x=range(0,8192)
        y=frame[0][self.slider.value()]
        self.graphWidget.plot(x, y)
        self.cur_frame.setText(str(self.slider.value()))

    def getSignal(self):
        global duration
        global frame
        wav = wave.open("Test2.wav", mode="r")#открываем файл
        count_of_samples_per_frame = 8192

        channels_num = wav.getnchannels()#Количество каналов
        sample_width = wav.getsampwidth()#Байт/сэмпл
        sample_rate = wav.getframerate()#Частота дискретизации, сэмплов/сек
        sample_num = wav.getnframes()#Количество сэмплов/кол-во каналов
        duration = sample_num / sample_rate#Длина трека

        #print(duration)
        #print(sample_num)s

        types = {1: np.int8,2: np.int16,4: np.int32}#Называется словарь, нужен для ↓
        content = wav.readframes(sample_num)#Считали все сэмплы в байтовую строку (байтовая строка: b'\x00\x00\x00\x00\...')
        samples = np.frombuffer(content, dtype=types[sample_width])#А затем преобразовали ее в массив (массив: [0,0,0,0,...])

        channel = []
        for i in range(channels_num):#Разбивание сэмплов на каналы
	        channel.append([])
	        for j in range(len(samples)//channels_num):
		        channel[i].append(samples[j*channels_num])

        frame = []
        for i in range(channels_num):
	        frame.append([])#Для каждого канала создаем подмассив кадров
	        for j in range(math.ceil(len(channel[i])/count_of_samples_per_frame)):
		        frame[i].append([])#Для каждого кадра создаем массив сэмплов
		        for k in range(j*count_of_samples_per_frame,count_of_samples_per_frame+j*count_of_samples_per_frame):
			        try:#Заполняем массив сэмплов сэмплами
				        frame[i][j].append(channel[i][k])
			        except:#Это происходит на последнем кадре. Так как для него больше нет сэмплов, забиваем все нулями
				        frame[i][j].append(0)
    


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
    main()