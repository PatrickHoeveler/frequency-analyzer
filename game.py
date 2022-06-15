from numpy import true_divide
import pyglet
import json
from pyglet import shapes

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()

circle = shapes.Circle(700, 150, 100, color=(
    50, 225, 30), batch=batch)
index = 0
with open('bass_hits.json') as f:
    bass_hits = json.load(f)



@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(dt):
    global index
    if(bass_hits[index] >= 1):
        print(index, bass_hits[index])
        circle.visible = True
        index += 1
    else:
        # print(index, bass_hits[index])
        circle.visible = False
        index += 100
    if(index>2000000):
        print(index)


if __name__ == '__main__':
    pyglet.gl.glClearColor(1, 1, 1, 1)
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()
