import math
import wave

import numpy as np


class Signal:
    def __init__(self, file):
        self.wav = wave.open(file, mode="r")  # Открываем файл, можно менять
        self.count_of_samples_per_frame = 16384  # Разрешение ДПФ, можно менять

        self.channels_num = self.wav.getnchannels()  # Количество каналов
        self.sample_width = self.wav.getsampwidth()  # Байт/сэмпл
        self.sample_rate = self.wav.getframerate()  # Частота дискретизации, сэмплов/сек
        self.sample_num = self.wav.getnframes()  # Количество сэмплов/кол-во каналов
        self.duration = self.sample_num / self.sample_rate  # Длина трека

        # print(self.duration)
        # print(self.sample_num)

        # Называется словарь, нужен для ↓
        self.types = {1: np.int8, 2: np.int16, 4: np.int32}
        self.content = self.wav.readframes(
            self.sample_num)  # Считали все сэмплы в байтовую строку (байтовая строка: b'\x00\x00\x00\x00\...')
        self.samples = np.frombuffer(self.content, dtype=self.types[
            self.sample_width])  # А затем преобразовали ее в массив (массив: [0,0,0,0,...])

        self.channel = []
        for i in range(self.channels_num):  # Разбивание сэмплов на каналы
            self.channel.append([])
            for j in range(len(self.samples) // self.channels_num):
                self.channel[i].append(self.samples[j * self.channels_num])

        self.channels_num = 1

        # Разбиваем на фреймы
        self.frame = []
        self.getFrames()

        # Считаем энергии кадров
        self.energy = []
        self.getEnery()

        # Считаем среднюю энергию всего трека
        average_energy = self.getAverageEnergy()

        # Удаляем пустые кадры
        self.deleteEmptyFrames(average_energy)

        # Провешиваем окно на кадры
        for i in range(len(self.frame)):
            for j in range(len(self.frame[i])):
                self.make_window(self.frame[i][j])

        # Считаем спектры кадров
        # Массив со спектральными отсчётами похож на массив с кадрами, только вместо семплов будут комплексные числа
        self.spectre = []
        self.makeSpectres()

        s1 = [32.7, 34.65, 36.71, 38.89, 41.2, 43.65,
              46.25, 49, 51.91, 55, 58.27, 61.74]
        s2 = ["C", "Cd", "D", "Dd", "E", "F", "Fd", "G", "Gd", "A", "Ad", "B"]
        notes = {}
        for i in range(1, 8):
            if i:
                for j in range(0, 12):
                    notes[s1[j]] = str(i) + s2[j]
                    s1[j] = s1[j] * 2

        reference_freq = list(notes.keys())
        spectre_freq = []

        for i in range(8129):
            spectre_freq.append(i * self.sample_rate /
                                self.count_of_samples_per_frame)

        ranges = [0]
        for i in range(len(reference_freq) - 1):
            ranges.append(
                asd((reference_freq[i] + reference_freq[i + 1]) / 2, spectre_freq))

        average_on_range = []
        for i in range(len(self.spectre)):
            average_on_range.append([])
            for j in range(len(self.spectre[i])):
                average_on_range[i].append([])
                for k in range(len(ranges) - 1):
                    left = ranges[k]
                    right = ranges[k + 1]
                    freq_range = list(self.spectre[i][j][left:right + 1])
                    self.make_window(freq_range)
                    if len(freq_range) > 1:
                        avereage_arifm = 0
                        for l in range(len(freq_range)):
                            avereage_arifm += freq_range[l]
                        avereage_arifm /= len(freq_range)
                    else:
                        avereage_arifm = freq_range[0]
                    average_on_range[i][j].append(avereage_arifm)

        self.maximum_freq_on_frame = []
        for i in range(len(average_on_range)):
            self.maximum_freq_on_frame.append([])
            for j in range(len(average_on_range[i])):
                maxim = 0
                index = 0
                for k in range(len(average_on_range[i][j])):
                    if (average_on_range[i][j][k] > maxim):
                        maxim = average_on_range[i][j][k]
                        index = k
                self.maximum_freq_on_frame[i].append(index)

        counts_of_repetition = []
        for i in range(1):
            for j in range(len(self.maximum_freq_on_frame[i])):
                k = search_for_repetition(
                    counts_of_repetition, notes[reference_freq[self.maximum_freq_on_frame[i][j]]])
                if k == -1:
                    counts_of_repetition.append(
                        [notes[reference_freq[self.maximum_freq_on_frame[i][j]]], 1])
                else:
                    counts_of_repetition[k][1] += 1

        k = 0
        self.most_frequently_encounted = []
        while(k < 3):
            max = 0
            index = 0
            for i in range(len(counts_of_repetition)):
                if counts_of_repetition[i][1] >= max:
                    max = counts_of_repetition[i][1]
                    index = i
            self.most_frequently_encounted.append(counts_of_repetition[index])
            del counts_of_repetition[index]
            k += 1
        print(self.most_frequently_encounted)

    def getFrames(self):
        for i in range(self.channels_num):
            # Для каждого канала создаем подмассив кадров
            self.frame.append([])
            for j in range(math.ceil(len(self.channel[i]) / self.count_of_samples_per_frame)):
                # Для каждого кадра создаем массив сэмплов
                self.frame[i].append([])
                for k in range(j * self.count_of_samples_per_frame,
                               self.count_of_samples_per_frame + j * self.count_of_samples_per_frame):
                    try:  # Заполняем массив сэмплов сэмплами
                        self.frame[i][j].append(self.channel[i][k])
                    except:  # Это происходит на последнем кадре. Так как для него больше нет сэмплов, забиваем все нулями
                        self.frame[i][j].append(0)

    def getEnery(self):
        for i in range(len(self.frame)):
            self.energy.append([])
            for j in range(len(self.frame[i])):
                sum = 0
                for k in range(len(self.frame[i][j])):
                    sum += abs(self.frame[i][j][k]) ^ 2
                self.energy[i].append(sum)

    def getAverageEnergy(self):
        average_energy = 0
        for i in range(len(self.energy)):
            for j in range(len(self.energy[i])):
                average_energy += int(self.energy[i][j])
        average_energy = average_energy / \
            (len(self.energy[0]) * len(self.energy))
        return average_energy

    def deleteEmptyFrames(self, average_energy):
        for i in range(len(self.energy)):
            j = 0
            while j < len(self.energy[i]):
                if self.energy[i][j] <= 0.3 * average_energy:
                    self.frame = np.delete(self.frame, j, 1)
                    self.energy = np.delete(self.energy, j, 1)
                    j -= 1
                j += 1

    def makeSpectres(self):
        for i in range(self.channels_num):
            self.spectre.append([])
            for j in range(len(self.frame[i])):
                self.spectre[i].append([])
                self.spectre[i][j] = self.FFT_vectorized(
                    self.frame[i][j])  # Считаем спектры

        for i in range(self.channels_num):
            for j in range(len(self.spectre[i])):
                for k in range(self.count_of_samples_per_frame):
                    self.spectre[i][j][k] = abs(self.spectre[i][j][k])
                self.spectre[i][j] = np.frombuffer(
                    self.spectre[i][j], dtype=np.float64)
                for k in range(1, len(self.spectre[i][j]) // 2):
                    self.spectre[i][j] = np.delete(self.spectre[i][j], k)
                self.spectre[i][j] = np.delete(
                    self.spectre[i][j], len(self.spectre[i][j]) - 1)

    def findMax(self):
        for i in range(len(self.spectre)):
            self.maximum_freq_on_frame.append([])
            for j in range(len(self.spectre[i])):
                maxim = 0
                index = 0
                for k in range(188):
                    if self.spectre[i][j][k] > maxim:
                        maxim = self.spectre[i][j][k]
                        index = k
                self.maximum_freq_on_frame[i].append(index)

    def getSignal(self):
        return self.frame

    def getSpectre(self):
        return self.spectre

    def getDuration(self):
        return self.duration

    def make_window(self, arr):
        for k in range(len(arr)):
            arr[k] = (0.54 - 0.46 * math.cos(
                (2 * math.pi * k) / len(arr))) * arr[k]

    def myFFT(self, x):
        x = np.asarray(x, dtype=float)
        N = x.shape[0]
        N = int(N)

        if N <= 32:
            return self.DFT_slow(x)
            """return np.concatenate([[x[0]+x[1]],[x[0]-x[1]]])"""
        else:
            X_even = self.myFFT(x[:N:2])
            X_odd = self.myFFT(x[1:N:2])
            factor = np.exp(-2j * np.pi * np.arange(N / 2) / N)
            t = factor * X_odd
            return np.concatenate([X_even + t, X_even - t])

    def DFT_slow(self, x):
        """Compute the discrete Fourier Transform of the 1D array x"""
        x = np.asarray(x, dtype=float)
        N = x.shape[0]
        n = np.arange(N)
        k = n.reshape((N, 1))
        M = np.exp(-2j * np.pi * k * n / N)
        return np.dot(M, x)

    def FFT_vectorized(self, x):
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

    def FFT(self, x):
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
        return (l)
    return (r)


def search_for_repetition(a, x):
    flag = False
    for i in range(len(a)):
        if a[i][0] == x:
            flag = True
            return i
    if flag == False:
        return -1
