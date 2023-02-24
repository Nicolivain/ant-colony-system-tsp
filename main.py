import yaml
import numpy as np
import matplotlib.lines
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from tsp import TSP
from acs import ACS
from animation import animate


matplotlib.use("TkAgg")

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.loader.SafeLoader)

tsp = TSP(**config)
points = tsp.get_nodes()
acs = ACS(tsp, 1)

fig, ax = plt.subplots()
ax.scatter(points[:, 0], points[:, 1])
plt.show()

for i in range(100):
    acs.step()
    value_matrix = acs.get_value_matrix()
    z = np.max(value_matrix)

    plt.clf()
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(points[:, 0], points[:, 1])
    for i in range(tsp.get_n_nodes()):
        for j in range(i + 1, tsp.get_n_nodes()):
            ax.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'r-', alpha=value_matrix[i, j]/z)

    plt.show()




"""
connections = []
for i in range(tsp.get_n_nodes()):
    for j in range(i+1, tsp.get_n_nodes()):
        connections.append(plt.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'r-', alpha=0)[0])


def anim(i):
    return animate(i, connections, config["dt"])


ani = animation.FuncAnimation(fig, anim, frames=config["n_frames"], interval=1000//config["fps"], blit=True, repeat=True)
"""