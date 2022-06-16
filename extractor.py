import json
import wave
import numpy as np
import matplotlib.pyplot as plt


filename = 'song.wav'

# filename = 'song-lowpass-100.wav'
# filename='song-midpass-100-5000.wav'
# filename='song-highpass-5000.wav'
# filename='kick.wav'

signal_wave = wave.open(filename, 'r')
# sample_rate = 16000
frame_rate = signal_wave.getframerate()
n_frames = signal_wave.getnframes()
print(signal_wave.getparams())

duration = n_frames/frame_rate
# print(duration)
window = frame_rate
# window = 10000
print(window)


# get 1 second of signal
signal = np.frombuffer(signal_wave.readframes(window), dtype=np.int16)

# sig = sig[0:1000]
# print(signal)

left, right = signal[0::2], signal[1::2]
# print(left)
# print(right)
# fft_spectrum = np.fft.rfft(signal)

# move from time to frequency domain
fft = np.fft.fft(left)

# phase and magnitude (complex number)
print(fft[0])
magnitude_spectrum = np.abs(fft)
print(magnitude_spectrum[0])


def plot_magnitue_spectrum(signal, sr, f_ratio=1):
    ft = np.fft.fft(signal)
    magnitude_spectrum = np.abs(ft)
    frequency = np.linspace(0, sr, len(magnitude_spectrum))
    num_frequency_bins = int(len(frequency) * f_ratio)

    plt.figure(figsize=(10,6))
    plt.plot(frequency[:num_frequency_bins], magnitude_spectrum[:num_frequency_bins])
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')
    plt.show()


plot_magnitue_spectrum(left, frame_rate, 0.05)

# max_left = max(left)
# left = left[1900000:2200000]

# left = [0 if x < 0 else x for x in left]
# print(len(left))
# threshold = max_left -max_left*0.25
# print(max_left)
# print(threshold)


# bass_hits = [int(max_left) if x > threshold else 0 for x in left]

# print(len([x for x in bass_hits if x > 0]))

# with open('bass_hits.json', 'w') as file:
    # json.dump(bass_hits, file)

# plot_a = plt.subplot(211)
# plot_a.plot(left)
# plot_a.plot(bass_hits)
# # plot_a.plot(right)

# plot_a.set_xlabel('frames')
# plot_a.set_ylabel('amplitude')
