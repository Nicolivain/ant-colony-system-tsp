import numpy as np
import matplotlib.pyplot as plt


def create_connections(n, points, ax):
    connections = []
    for i in range(n):
        for j in range(i + 1, n):
            connections.append(ax.plot([points[i, 0], points[j, 0]], [points[i, 1], points[j, 1]], 'r-', alpha=0)[0])
    return connections


def create_best_path(nodes, path, ax):
    vertexes = []
    for i in range(-1, len(path)-1):
        vp, vn = path[i], path[i+1]
        vertexes = vertexes + ax.plot([nodes[vp, 0], nodes[vn, 0]], [nodes[vp, 1], nodes[vn, 1]], 'g-')
    return vertexes


def update_alpha(value_matrix, connections):
    value_matrix = value_matrix / np.sum(value_matrix, axis=1)
    k = 0
    for i in range(value_matrix.shape[0]):
        for j in range(i+1, value_matrix.shape[0]):
            connections[k].set_alpha(value_matrix[i, j])
            k += 1
    return connections


def update_best_path(nodes, path, vertexes):
    for i in range(-1, len(path)-1):
        vp, vn = path[i], path[i+1]
        vertexes[i+1].set_xdata([nodes[vp, 0], nodes[vn, 0]])
        vertexes[i].set_ydata([nodes[vp, 1], nodes[vn, 1]])
    return vertexes


def create_animation_figure(tsp, acs):
    fig, axs = plt.subplots(1, 2, figsize=(20, 10))
    nodes = tsp.get_nodes()
    axs[0].scatter(nodes[:, 0], nodes[:, 1])
    axs[0].set_title("Vertex Probabilities")
    axs[1].scatter(nodes[:, 0], nodes[:, 1])
    axs[1].set_title("Best Path")
    connections = create_connections(tsp.get_n_nodes(), nodes, axs[0])
    best_path = create_best_path(nodes, acs.get_current_best_path()[0], axs[1])
    return fig, axs, connections, best_path


def animate(connections, best_path, nodes, acs, steps_per_frame=1):
    for k in range(steps_per_frame):
        acs.step()
    connections = update_alpha(acs.get_value_matrix(), connections)
    vertexes = update_best_path(nodes, acs.get_current_best_path()[0], best_path)
    return connections + vertexes
