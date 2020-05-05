import wave
import numpy as np
import math

def FFT(x):
    """A recursive implementation of the 1D Cooley-Tukey FFT"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    N = int(N)
    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    elif N <= 32:  # this cutoff should be optimized
        return DFT_slow(x)
    else:
        X_even = FFT(x[::2])
        X_odd = FFT(x[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        return np.concatenate([X_even + factor[:N // 2] * X_odd,
                               X_even + factor[N // 2:] * X_odd])
def DFT_slow(x):
    """Compute the discrete Fourier Transform of the 1D array x"""
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)

wav = wave.open("Test4.wav", mode="r")#Открываем файл, можно менять
count_of_samples_per_frame = 8192#Разрешение ДПФ, можно менять

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
for i in frame[0][1]: #Так мы можем посмотреть на первый кадр нулевого канала (есть еще нулевой кадр, я отсчет веду с нуля всегда)
	print (i)
'''

spectre = []#Массив со спектрами похож на массив с кадрами, только вместо сымплов будут комплексные числа (спектры)
for i in range(channels_num):
	spectre.append([])
	for j in range(len(frame[i])):
		spectre[i].append([])
		spectre[i][j]=FFT(frame[i][j])#Считаем спектры
'''
for i in spectre[0][1]: #Так увидим вектор спектра первого кадра нулевого канала
	print(i)
'''

for i in range(channels_num):
	for j in range(len(spectre[i])):
		for k in range(count_of_samples_per_frame):
			spectre[i][j][k] = abs(spectre[i][j][k])
		spectre[i][j] = np.frombuffer(spectre[i][j], dtype=np.float64)
		for k in range(1,len(spectre[i][j])//2):
			spectre[i][j] = np.delete(spectre[i][j],k)
		spectre[i][j] = np.delete(spectre[i][j], len(spectre[i][j])-1)
'''
for i in spectre[0][1]: #Теперь в массиве спектров хранятся модули этих спектров
	print(i)
'''