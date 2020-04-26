import wave
import numpy as np
import math

wav = wave.open("4.wav", mode="r")#открываем файл
count_of_samples_per_frame = 8192

channels_num = wav.getnchannels()#Количество каналов
sample_width = wav.getsampwidth()#Байт/сэмпл
sample_rate = wav.getframerate()#Частота дискретизации, сэмплов/сек
sample_num = wav.getnframes()#Количество сэмплов/кол-во каналов
duration = sample_num / sample_rate#Длина трека

print(duration)
print(sample_num)

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
'''
for i in frame[0][1]: #так мы можем посмотреть на первый кадр нулевого канала (есть еще нулевой кадр, я отсчет веду с нуля всегда)
	print (i)

'''