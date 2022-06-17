import sys
import pyglet
import sounddevice as sd
import librosa
import numpy as np
import progressbar
from pyglet import shapes

import processor

window = pyglet.window.Window(1200, 800)
batch = pyglet.graphics.Batch()

# circle = shapes.Circle(700, 150, 100, color=(
#     50, 225, 30), batch=batch)
# line = shapes.Line(10, 10, 10, 20, width=1, color=(255, 0, 0), batch=batch)

devices = sd.query_devices()

for i in range(len(devices)):
    # if("Scarlett Solo USB" in devices[i]['name']):
    #     print(i, devices[i]['name'])
    if(devices[i]['max_output_channels'] > 0):
        print(i, devices[i]['name'])
    # print(i, devices[i])

print(devices[9])
sr = devices[9]['default_samplerate']
print(sd.default.device)
# data, fs = sf.read(args.filename, dtype='float32')
# signal, sr = librosa.load('kick.wav', sr=48000)
# sd.play(signal, sr, device=9)
# status = sd.wait()
bass_lvl = 0

blocksize=512

frequencies = []
lines = []

bar = progressbar.ProgressBar(maxval=100,
                              widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

# def callback(indata, frames, time, status):


def callback(indata, outdata, frames, time, status):
    global frequencies
    print(len(indata))
    if status:
        print(status)
    # print(len(outdata))
    if status:
        print(status)

    if(np.any(indata)):
        print(indata)
        # frequencies = processor.get_frequencies(indata)
        # print(frequencies)
        # print(np.amax(indata), end='\r')
        # outdata[:] = indata
        # bass_lvl = processor.check_bass(signal=indata, sr=sr)
        frequencies = processor.get_frequencies(signal=indata, sr=sr)
        # frequencies = indata
        # frequencies = np.abs(librosa.stft(indata, n_fft=blocksize))

        # print(bass_lvl)
        # print(bass_lvl, end = "\r")
        outdata[:] = indata
        # update(bass_lvl)
        # processor.plot_bass(signal=indata, sr=sr)
    # print(status)
    # print(frames)
    # print(time)
    # print(status)

# stream = sd.Stream(channels=2, callback=callback, samplerate=sr, blocksize=1024)


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
            lines[i].y2 = frequencies[i][0]*200+100



with sd.Stream(device=[5, 15], callback=callback, blocksize=blocksize, channels=2):
    # with sd.InputStream(device=7, channels=2, callback=callback):
    # sd.sleep(100)
    init_lines(blocksize)

    pyglet.gl.glClearColor(1, 1, 1, 1)
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()

    while(True):
        sd.sleep(1000)
