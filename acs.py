import yaml
import numpy as np
import matplotlib.pyplot as plt

from ant import Ant


def get_greedy_path(value_matrix, cost_matrix=None):
    cost_matrix = value_matrix if cost_matrix is None else cost_matrix
    current = 0
    path = [0]
    total_cost = 0
    while len(path) < value_matrix.shape[0]:
        values = value_matrix[current, :]
        mask = np.ones_like(values)
        mask[path] = 0
        next_node = np.nanargmax(mask * values)
        path.append(next_node)
        total_cost += cost_matrix[current, next_node]
        current = next_node
    return path, total_cost


def plot_path(nodes, path):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(nodes[:, 0], nodes[:, 1])
    for i in range(-1, len(path)-1):
        vp, vn = path[i], path[i+1]
        ax.plot([nodes[vp, 0], nodes[vn, 0]], [nodes[vp, 1], nodes[vn, 1]], 'g-')
    return ax


class ACS:
    def __init__(self, tsp, n_agents):
        self._tsp = tsp
        self._n_agents = n_agents
        with open("config.yaml") as f:
            consts = yaml.load(f, Loader=yaml.loader.SafeLoader)

        self._pheromone_impact = consts["pheromone_impact"]
        self._dist_impact = consts["distance_impact"]
        self._exploration_rate = consts["exploration_rate"]
        self._lr = consts["learning_rate"]

        self._dist_matrix = self._tsp.get_dist_matrix()
        self._pheromones_matrix = np.ones_like(self._dist_matrix) / tsp.get_n_nodes() ** 2

        self._local_pheromone_update = consts["local_pheromone_update"]
        self._local_pheromone_update = self._local_pheromone_update if self._local_pheromone_update > 0 else 1 / tsp.get_n_nodes() / get_greedy_path(1/self._dist_matrix, self._dist_matrix)[1]

        start_pos = np.random.randint(0, tsp.get_n_nodes(), n_agents)
        self._ants = [Ant(start_index=s, pheromone_impact=self._pheromone_impact, dist_impact=self._dist_impact, exploration_rate=self._exploration_rate) for s in start_pos]

    def step(self):
        for ant in self._ants:
            pos = ant.get_current_pos()
            ant.move(self._dist_matrix[pos, :], self._pheromones_matrix[pos, :])

            # local updating of the pheromones
            vp, vn = ant.get_last_vertex()
            self._locally_update_pheromone(vp, vn)

        # we check if the ants have finished their lap, note that all finish at the same time
        if self._ants[0].finished_lap():
            for ant in self._ants:
                path = ant.get_path()
                delta_pheromones = 1 / ant.get_total_cost()
                self._globally_update_pheromone(path, delta_pheromones)

    def get_current_best_path(self):
        value_matrix = (1 / self._dist_matrix)**self._dist_impact * self._pheromones_matrix**self._pheromone_impact
        return get_greedy_path(value_matrix, self._dist_matrix)

    def get_value_matrix(self):
        return (1 / self._dist_matrix)**self._dist_impact * self._pheromones_matrix**self._pheromone_impact

    def get_dist_matrix(self):
        return self._dist_matrix

    def get_pheromone_matrix(self):
        return self._pheromones_matrix

    def _locally_update_pheromone(self, i, j):
        self._pheromones_matrix[i, j] = (1 - self._lr) * self._pheromones_matrix[i, j] + self._lr * self._local_pheromone_update
        self._pheromones_matrix[j, i] = (1 - self._lr) * self._pheromones_matrix[i, j] + self._lr * self._local_pheromone_update

    def _globally_update_pheromone(self, path, delta_pheromones):
        for i in range(len(path)-1):
            vp, vn = path[i], path[i+1]
            self._pheromones_matrix[vn, vp] = (1 - self._lr) * self._pheromones_matrix[vn, vp] + self._lr * delta_pheromones
            self._pheromones_matrix[vn, vp] = (1 - self._lr) * self._pheromones_matrix[vn, vp] + self._lr * delta_pheromones






