import yaml
import numpy as np


class ACS:
    def __init__(self, tsp, n_agents):
        self._tsp = tsp
        self._n_agents = n_agents
        with open("config.yaml") as f:
            consts = yaml.load(f, Loader=yaml.loader.SafeLoader)

        self._pheromone_impact = consts["PHEROMONE_IMPACT"]
        self._dist_impact = consts["DIST_IMPACT"]

        self.ants = []

    def step(self):
        pass






