import numpy as np
import librosa
import matplotlib.pyplot as plt

FRAME_SIZE = 2048
HOP_SIZE = 512


def get_frequencies(signal, sr):
    # sr = int(sr/2)
    ft = np.fft.fft(signal)
    magnitude_spectrum = np.abs(ft)
    for i in range(sr-len(magnitude_spectrum)):
        magnitude_spectrum = np.append(magnitude_spectrum, 0)
    # magnitude_spectrum = magnitude_spectrum[:20000]
    # print(np.amax(magnitude_spectrum))
    # frequency = np.linspace(0, sr, len(magnitude_spectrum))
    # num_frequency_bins = int(len(frequency) * f_ratio)
    # otherwise freqs are mirrored
    # magnitude_spectrum = magnitude_spectrum[:int(len(frequency)/2)]
    return magnitude_spectrum


def check_bass(signal, sr):
    freq_filter = 100
    ft = np.fft.fft(signal)
    # print(ft)
    magnitude_spectrum = np.abs(ft)
    # print(np.amax(magnitude_spectrum))
    frequency = np.linspace(0, sr, len(magnitude_spectrum))
    # num_frequency_bins = int(len(frequency) * f_ratio)
    frequency = [x for x in frequency if x < freq_filter]
    magnitude_spectrum = magnitude_spectrum[:len(frequency)]
    if(np.any(magnitude_spectrum>0.7)):
        # print("bass detected", np.amax(magnitude_spectrum))
        return np.amax(magnitude_spectrum)
    return 0




def plot_bass(signal, sr):
    sr = sr/2
    # mono
    signal = [x[0] for x in signal]
    ft = np.fft.fft(signal)
    magnitude_spectrum = np.abs(ft)
    frequency = np.linspace(0, sr, 22000)
    # num_frequency_bins = int(len(frequency) * f_ratio)
    # frequency = [x for x in frequency if x < 22000]
    for i in range(len(frequency)-len(magnitude_spectrum)):
        magnitude_spectrum = np.append(magnitude_spectrum, 0)

    print(len(frequency), len(magnitude_spectrum))

    plt.figure(figsize=(10,6))
    plt.plot(frequency, magnitude_spectrum)
    # plt.plot(frequency[:num_frequency_bins], magnitude_spectrum[:num_frequency_bins])
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')
    plt.show()