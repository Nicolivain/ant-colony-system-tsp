import yaml
import numpy as np
import matplotlib.lines
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from tsp import TSP
from animation import animate


matplotlib.use("TkAgg")

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.loader.SafeLoader)

tsp = TSP(**config)
points = tsp.get_nodes()

fig = plt.figure()
plt.scatter(points[:, 0], points[:, 1])

connections = []
for i in range(tsp.get_n_nodes()):
    for j in range(i+1, tsp.get_n_nodes()):
        connections.append(plt.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'r-', alpha=0)[0])


def anim(i):
    return animate(i, connections, config["dt"])


ani = animation.FuncAnimation(fig, anim, frames=config["n_frames"], interval=1000//config["fps"], blit=True, repeat=True)

plt.show()
