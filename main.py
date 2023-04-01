import yaml
import datetime
import matplotlib.lines
import matplotlib.animation as animation

from tsp import TSP
from acs import ACS, get_greedy_path
from animation import create_animation_figure, animate


matplotlib.use("Agg")

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.loader.SafeLoader)

tsp = TSP(**config)
nodes = tsp.get_nodes()
acs = ACS(tsp, config["n_agent"])

path, tc = get_greedy_path(value_matrix=acs.get_inv_dist_matrix(), cost_matrix=acs.get_dist_matrix())
fig, axs, connections, best_path = create_animation_figure(tsp, acs)
print(tc)


def anim(i):
    return animate(connections, best_path, nodes, acs, steps_per_frame=config["n_steps"] // config["n_frames"])


time_start = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
ani = animation.FuncAnimation(fig, anim, frames=config["n_frames"], interval=1000//config["fps"], blit=True, repeat=False)
writer = animation.PillowWriter(fps=config["fps"])
ani.save(f'animations/{time_start}.gif', writer=writer)

print(acs.get_current_best_path())
print("done")
