import yaml
import numpy as np
import matplotlib.lines
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from tsp import TSP
from acs import ACS, get_greedy_path, plot_path
from animation import create_animation_figure, update_alpha, update_best_path, animate


matplotlib.use("TkAgg")

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.loader.SafeLoader)

tsp = TSP(**config)
nodes = tsp.get_nodes()
acs = ACS(tsp, config["n_agent"])

path, tc = get_greedy_path(value_matrix=acs.get_inv_dist_matrix(), cost_matrix=acs.get_dist_matrix())
fig, axs, connections, best_path = create_animation_figure(tsp, acs)
print(tc)



def anim(i):
    print(i)
    return animate(connections, best_path, nodes, acs, steps_per_frame=10)


ani = animation.FuncAnimation(fig, anim, frames=config["n_frames"], interval=1000//config["fps"], blit=True, repeat=True)
plt.show()

print(tc)
print("done")

"""
connections = []
for i in range(tsp.get_n_nodes()):
    for j in range(i+1, tsp.get_n_nodes()):
        connections.append(plt.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'r-', alpha=0)[0])



"""