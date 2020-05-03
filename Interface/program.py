import wave
import numpy as np
import math

class Signal:
	def __init__(self,file):
		self.wav = wave.open(file, mode="r")#Открываем файл, можно менять
		self.count_of_samples_per_frame = 8192#Разрешение ДПФ, можно менять

		self.channels_num = self.wav.getnchannels()#Количество каналов
		self.sample_width = self.wav.getsampwidth()#Байт/сэмпл
		self.sample_rate = self.wav.getframerate()#Частота дискретизации, сэмплов/сек
		self.sample_num = self.wav.getnframes()#Количество сэмплов/кол-во каналов
		self.duration = self.sample_num / self.sample_rate#Длина трека

		#print(self.duration)
		#print(self.sample_num)

		self.types = {1: np.int8,2: np.int16,4: np.int32}#Называется словарь, нужен для ↓
		self.content = self.wav.readframes(self.sample_num)#Считали все сэмплы в байтовую строку (байтовая строка: b'\x00\x00\x00\x00\...')
		self.samples = np.frombuffer(self.content, dtype=self.types[self.sample_width])#А затем преобразовали ее в массив (массив: [0,0,0,0,...])

		self.channel = []
		for i in range(self.channels_num):#Разбивание сэмплов на каналы
			self.channel.append([])
			for j in range(len(self.samples)//self.channels_num):
				self.channel[i].append(self.samples[j*self.channels_num])

		self.frame = []
		for i in range(self.channels_num):
			self.frame.append([])#Для каждого канала создаем подмассив кадров
			for j in range(math.ceil(len(self.channel[i])/self.count_of_samples_per_frame)):
				self.frame[i].append([])#Для каждого кадра создаем массив сэмплов
				for k in range(j*self.count_of_samples_per_frame,self.count_of_samples_per_frame+j*self.count_of_samples_per_frame):
					try:#Заполняем массив сэмплов сэмплами
						self.frame[i][j].append(self.channel[i][k])
					except:#Это происходит на последнем кадре. Так как для него больше нет сэмплов, забиваем все нулями
						self.frame[i][j].append(0)

		self.make_window()

		self.spectre = []#Массив со спектрами похож на массив с кадрами, только вместо сымплов будут комплексные числа
		for i in range(self.channels_num):
			self.spectre.append([])
			for j in range(len(self.frame[i])):
				self.spectre[i].append([])
				self.spectre[i][j]=self.FFT_vectorized(self.frame[i][j])#Считаем спектры

		for i in range(self.channels_num):
			for j in range(len(self.spectre[i])):
				for k in range(self.count_of_samples_per_frame):
					self.spectre[i][j][k] = abs(self.spectre[i][j][k])
				self.spectre[i][j] = np.frombuffer(self.spectre[i][j], dtype=np.float64)
				for k in range(1,len(self.spectre[i][j])//2):
					self.spectre[i][j] = np.delete(self.spectre[i][j],k)
				self.spectre[i][j] = np.delete(self.spectre[i][j], len(self.spectre[i][j])-1)

	def FFT_vectorized(self,x):
		"""A vectorized, non-recursive version of the Cooley-Tukey FFT"""
		x = np.asarray(x, dtype=float)
		N = x.shape[0]

		if np.log2(N) % 1 > 0:
		    raise ValueError("size of x must be a power of 2")
		
		# N_min here is equivalent to the stopping condition above,
		# and should be a power of 2
		N_min = min(N, 32)

		# Perform an O[N^2] DFT on all length-N_min sub-problems at once
		n = np.arange(N_min)
		k = n[:, None]
		M = np.exp(-2j * np.pi * n * k / N_min)
		X = np.dot(M, x.reshape((N_min, -1)))
		# build-up each level of the recursive calculation all at once
		while X.shape[0] < N:
		    X_even = X[:, :X.shape[1] // 2]
		    X_odd = X[:, X.shape[1] // 2:]
		    factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
		                    / X.shape[0])[:, None]
		    X = np.vstack([X_even + factor * X_odd,
		                   X_even - factor * X_odd])
		return X.ravel()

	def getSignal(self):
		return self.frame

	def getSpectre(self):
		return self.spectre

	def getDuration(self):
		return self.duration

	def make_window(self):
		for i in range(len(self.frame)):
			for j in range(len(self.frame[i])):
				for k in range(len(self.frame[i][j])):
					self.frame[i][j][k]=(0.54-0.46*math.cos((2*math.pi*k)/self.count_of_samples_per_frame))*self.frame[i][j][k]

	def myFFT(self,x):
		x=np.asarray(x,dtype=float)
		N=x.shape[0]
		N=int(N)
	
		if N==2:
			return np.concatenate([[x[0]+x[1]],[x[0]-x[1]]])
		else:
			X_even= self.myFFT(x[:N:2])
			X_odd= self.myFFT(x[1:N:2])
			factor = np.exp(-2j * np.pi * np.arange(N/2) / N)
			return np.concatenate([X_even+factor*X_odd,X_even-factor*X_odd])

	def FFT(self,x):
	    """A recursive implementation of the 1D Cooley-Tukey FFT"""
	    x = np.asarray(x, dtype=float)
	    N = x.shape[0]
	    N = int(N)
	    if N % 2 > 0:
	        raise ValueError("size of x must be a power of 2")
	    elif N == 32:  # this cutoff should be optimized
	        return self.DFT_slow(x)
	    else:
	        X_even = self.FFT(x[::2])
	        X_odd = self.FFT(x[1::2])
	        factor = np.exp(-2j * np.pi * np.arange(N) / N)
	        return np.concatenate([X_even + factor[:N // 2] * X_odd,
	                               X_even + factor[N // 2:] * X_odd])
	def DFT_slow(self,x):
	    """Compute the discrete Fourier Transform of the 1D array x"""
	    x = np.asarray(x, dtype=float)
	    N = x.shape[0]
	    n = np.arange(N)
	    k = n.reshape((N, 1))
	    M = np.exp(-2j * np.pi * k * n / N)
	    return np.dot(M, x)


'''
for i in frame[0][1]: #Так мы можем посмотреть на первый кадр нулевого канала (есть еще нулевой кадр, я отсчет веду с нуля всегда)
	print (i)


spectre = []#Массив со спектрами похож на массив с кадрами, только вместо сымплов будут комплексные числа (спектры)
for i in range(channels_num):
	spectre.append([])
	for j in range(len(frame[i])):
		spectre[i].append([])
		spectre[i][j]=FFT(frame[i][j])#Считаем спектры

for i in spectre[0][1]: #Так увидим вектор спектра первого кадра нулевого канала
	print(i)


for i in range(channels_num):
	for j in range(len(spectre[i])):
		for k in range(count_of_samples_per_frame):
			spectre[i][j][k] = abs(spectre[i][j][k])
		spectre[i][j] = np.frombuffer(spectre[i][j], dtype=np.float64)
		for k in range(1,len(spectre[i][j])//2):
			spectre[i][j] = np.delete(spectre[i][j],k)
		spectre[i][j] = np.delete(spectre[i][j], len(spectre[i][j])-1)

for i in spectre[0][1]: #Теперь в массиве спектров хранятся модули этих спектров
	print(i)
'''