import sys
import pyglet
import sounddevice as sd
import librosa
import numpy as np
import progressbar
from pyglet import shapes
import json

import processor

window = pyglet.window.Window(1200, 800)
batch = pyglet.graphics.Batch()
bass_lvl = 0
blocksize=1024

# circle = shapes.Circle(700, 150, 100, color=(
#     50, 225, 30), batch=batch)
# line = shapes.Line(10, 10, 10, 20, width=1, color=(255, 0, 0), batch=batch)

devices = sd.query_devices()

for i in range(len(devices)):
    # if("Scarlett Solo USB" in devices[i]['name']):
    #     print(i, devices[i]['name'])
    # if(devices[i]['max_output_channels'] > 0):
    print(i, devices[i]['name'])
    # print(i, devices[i])

print(devices[9])
sr = devices[9]['default_samplerate']
print(sd.default.device)
# data, fs = sf.read(args.filename, dtype='float32')
# signal, sr = librosa.load('kick.wav', sr=48000)
# sd.play(signal, sr, device=9)
# status = sd.wait()

frequencies = []
lines = []
print('sr', sr)
# def callback(indata, frames, time, status):


def callback(indata, outdata, frames, time, status):
    global frequencies
    

    if(np.any(indata)):

        # with open('indata.json', 'w') as file:
        #     json.dump({'indata':indata.tolist()}, file)


        # frequencies = processor.get_frequencies(signal=indata, sr=blocksize)
        fft = np.array([x[0]/10 for x in indata])
        # print(fft)
        fft = fft * np.hamming(len(fft))
        # print(np.abs(np.fft.rfft(frequencies)[1:]))
        # fft = np.abs(np.fft.fft(fft))
        fft = np.abs(np.fft.rfft(fft))
        # fft = fft[:int(len(fft))]
        frequencies = fft
        # print(len(mags))
        


        # processor.plot_bass(signal=indata, sr=sr)

        # with open('frequencies.json', 'w') as file:
        #     json.dump({'frequencies': frequencies.tolist()}, file)
        # sys.exit()
        # print(frequencies)
        # frequencies = np.abs(librosa.stft(frequencies, n_fft=blocksize))
        # print(frequencies)

        # print(bass_lvl)
        # print(bass_lvl, end = "\r")

        outdata[:] = indata
        # outdata[:] = frequencies



@window.event
def on_draw():
    window.clear()
    batch.draw()


def init_lines(size):
    global lines
    for i in range(size):
        lines.append(shapes.Line(
            i+100, 100, i+100, 120, width=1, color=(255, 0, 0), batch=batch))


def update(dt):
    # print(bass_lvl)
    global frequencies
    global lines

    if(np.any(frequencies)):
        # print(len(frequencies))
        for i in range(len(lines)):
            # print(frequencies[i][0]*100+10)
            # lines[i].y2 = frequencies[i][0]*100+100
            lines[i].y2 = frequencies[i]*100+100


# device = ['CABLE OUTPUT', 'Scarlett Solo USB']

with sd.Stream(device=[5, 15], callback=callback, blocksize=blocksize, channels=2):
    # with sd.InputStream(device=7, channels=2, callback=callback):
    # sd.sleep(100)

    init_lines(int(blocksize/2))

    pyglet.gl.glClearColor(1, 1, 1, 1)
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()

    while(True):
        sd.sleep(1000)
