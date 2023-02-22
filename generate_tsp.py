import numpy as np


def generate_tsp(n, xmax=100, ymax=100):
    xs = np.random.uniform(0, xmax, n).reshape(-1, 1)
    ys = np.random.uniform(0, ymax, n).reshape(-1, 1)
    coords = np.concatenate([xs, ys], axis=1)
    return coords


