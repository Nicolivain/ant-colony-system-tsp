import numpy as np


class TSP:
    def __init__(self, n_nodes, xmax=100, ymax=100, **kwargs):
        xs = np.random.uniform(0, xmax, n_nodes).reshape(-1, 1)
        ys = np.random.uniform(0, ymax, n_nodes).reshape(-1, 1)

        self._n_nodes = n_nodes
        self._coords = np.concatenate([xs, ys], axis=1)

        self._dist_matrix = np.zeros(self._n_nodes, self._n_nodes)
        for i in range(self._n_nodes):
            for j in range(self._n_nodes):
                self._dist_matrix[i][j] = np.sqrt((self._coords[i, 0] - self._coords[j, 0]) ** 2 + (self._coords[i, 1] - self._coords[j, 1]) ** 2)

    def get_distances(self, i):
        return self._dist_matrix[i, :]

    def get_nodes(self):
        return self._coords
