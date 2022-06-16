import sounddevice as sd

devices = sd.query_devices()

# for d in devices:
#     print(d['hostapi'], d['name'])

print(devices[9]['name'])

def processing(outdata, frames, time, status):
    print(outdata)
    print(frames)
    print(time)
    print(status)

with sd.OutputStream(device=9, callback=processing, channels=2):
    sd.sleep(1000)