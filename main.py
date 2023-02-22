import yaml
import numpy as np
import matplotlib.lines
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from generate_tsp import generate_tsp
from animation import animate


matplotlib.use("TkAgg")

with open("config.yaml") as f:
    consts = yaml.load(f, Loader=yaml.loader.SafeLoader)
    locals().update(consts)

points = generate_tsp(NSTOPS)
print(type(points))
fig = plt.figure()
plt.scatter(points[:, 0], points[:, 1])

connections = []
for i in range(NSTOPS):
    for j in range(i+1, NSTOPS):
        connections.append(plt.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'r-', alpha=0)[0])

def anim(i):
    return animate(i, connections, DT)

ani = animation.FuncAnimation(fig, anim, frames=NFRAMES, interval=1000//FPS, blit=True, repeat=True)

plt.show()


