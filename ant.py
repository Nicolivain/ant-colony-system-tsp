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

    def move(self, distances, pheromones):
        if self._finished_lap:
            self._current_pos = self._start_index
            self._memory = [self._start_index]

        mask = np.ones_like(distances)
        mask[self._memory] = 0

        probs = mask * (1/distances)**self._dist_impact * pheromones**self._p_impact
        probs = probs / np.nansum(probs)
        probs[np.isnan(probs)] = 0
        if np.random.random() < self._exploration_rate:
            new_pos = np.random.choice(range(distances.shape[0]), p=probs)
        else:
            new_pos = np.nanargmax(probs)

        self._previous_pos = self._current_pos
        self._current_pos = new_pos
        self._memory.append(new_pos)
        self._total_cost += distances[new_pos]

        if self._current_pos == self._start_index:
            self._finished_lap = True
        else:
            self._finished_lap = False

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
