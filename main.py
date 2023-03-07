import yaml
import numpy as np
import matplotlib.lines
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from tsp import TSP
from acs import ACS, get_greedy_path, plot_path
from animation import animate


matplotlib.use("TkAgg")

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.loader.SafeLoader)

tsp = TSP(**config)
points = tsp.get_nodes()
acs = ACS(tsp, config["n_agent"])

path, tc = get_greedy_path(value_matrix=acs.get_inv_dist_matrix(), cost_matrix=acs.get_dist_matrix())
ax = plot_path(points, path)
print(tc)
plt.show()

for k in range(1000):
    acs.step()

path, tc = get_greedy_path(value_matrix=acs.get_value_matrix(), cost_matrix=acs.get_dist_matrix())
ax = plot_path(points, path)
print(tc)
plt.show()

print("done")

"""
connections = []
for i in range(tsp.get_n_nodes()):
    for j in range(i+1, tsp.get_n_nodes()):
        connections.append(plt.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'r-', alpha=0)[0])


def anim(i):
    return animate(i, connections, config["dt"])


ani = animation.FuncAnimation(fig, anim, frames=config["n_frames"], interval=1000//config["fps"], blit=True, repeat=True)
"""