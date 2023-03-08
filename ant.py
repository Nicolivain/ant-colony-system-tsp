import numpy as np


class Ant:
    def __init__(self, start_index, pheromone_impact, dist_impact, exploration_rate):
        self._memory = [start_index]
        self._total_cost = 0

        self._start_index = start_index
        self._current_pos = start_index
        self._previous_pos = None

        self._p_impact = pheromone_impact
        self._dist_impact = dist_impact
        self._exploration_rate = exploration_rate

        self._finished_lap = False

    def reset(self):
        self._current_pos = self._start_index
        self._previous_pos = None
        self._memory = [self._start_index]
        self._total_cost = 0

    def move(self, inv_distances, pheromones):
        mask = np.ones_like(inv_distances)
        mask[self._memory] = 0

        probs = mask * inv_distances**self._dist_impact * pheromones**self._p_impact
        probs = probs / np.nansum(probs)
        probs[np.isnan(probs)] = 0
        if np.random.random() < self._exploration_rate:
            new_pos = np.random.choice(range(inv_distances.shape[0]), p=probs)
        else:
            new_pos = np.nanargmax(probs)

        self._previous_pos = self._current_pos
        self._current_pos = new_pos
        self._memory.append(new_pos)
        self._total_cost += 1/(inv_distances[new_pos])

    def get_current_pos(self):
        return self._current_pos

    def get_last_vertex(self):
        return self._previous_pos, self._current_pos

    def get_total_cost(self):
        return self._total_cost

    def get_path(self):
        return self._memory

    def finished_lap(self):
        return self._finished_lap
