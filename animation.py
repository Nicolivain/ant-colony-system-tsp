import numpy as np


def animate(step, connections, dt):
    t = step * dt
    for c in connections:
        c.set_alpha(t)
    return connections
