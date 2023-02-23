import yaml
import numpy as np

from ant import Ant


class ACS:
    def __init__(self, tsp, n_agents):
        self._tsp = tsp
        self._n_agents = n_agents
        with open("config.yaml") as f:
            consts = yaml.load(f, Loader=yaml.loader.SafeLoader)

        self._pheromone_impact = consts["pheromone_impact"]
        self._dist_impact = consts["dist_impact"]
        self._exploration_rate = consts["exploration_rate"]
        self._lr = consts["learning_rate"]

        self._local_pheromone_update = consts["local_pheromone_update"]
        self._local_pheromone_update = self._local_pheromone_update if self._local_pheromone_update > 0 else 1 / tsp.get_n_nodes() / 500  # todo: replace 500 with greedy solution

        self._dist_matrix = self._tsp.get_dist_matrix()
        self._pheromones_matrix = np.ones_like(self._dist_matrix) / tsp.get_n_nodes()**2

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
            total_costs = [ant.get_total_cost() for ant in self._ants]
            best_idx = np.argmin(total_costs)
            delta_pheromones = 1 / total_costs[best_idx]
            best_path = self._ants[best_idx].get_path()
            self._globally_update_pheromone(best_path, delta_pheromones)

    def _locally_update_pheromone(self, i, j):
        self._pheromones_matrix[i, j] = (1 - self._lr) * self._pheromones_matrix[i, j] + self._lr * self._local_pheromone_update
        self._pheromones_matrix[j, i] = (1 - self._lr) * self._pheromones_matrix[i, j] + self._lr * self._local_pheromone_update

    def _globally_update_pheromone(self, path, delta_pheromones):
        for i in range(len(path)-1):
            vp, vn = path[i], path[i+1]
            self._pheromones_matrix[vn, vp] = (1 - self._lr) * self._pheromones_matrix[vn, vp] + self._lr * delta_pheromones
            self._pheromones_matrix[vn, vp] = (1 - self._lr) * self._pheromones_matrix[vn, vp] + self._lr * delta_pheromones






