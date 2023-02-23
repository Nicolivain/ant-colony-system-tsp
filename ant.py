import numpy as np


class Ant:
    def __init__(self, start_index, pheromone_impact, dist_impact):
        self._memory = [start_index]
        self._start_index = start_index
        self._current_pos = start_index
        self._p_impact = pheromone_impact
        self._dist_impact = dist_impact

    def move(self, distances, pheromones):
        mask = np.ones_like(distances)
        mask[self._memory] = 0

        probs = mask * distances**self._dist_impact * pheromones**self._p_impact
        probs = probs / np.sum(probs)

        new_pos = np.random.choice(range(distances.shape[0]), p=probs)
        self._memory.append(new_pos)

        self.check_turn_completed()

    def check_turn_completed(self):
        pass

    def get_current_pos(self):
        return self._current_pos

