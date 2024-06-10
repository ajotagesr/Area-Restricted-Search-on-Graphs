import networkx as nx
import numpy as np
import pylab
import random

from typing import Any
from matplotlib import pyplot as plt


PAGERANK_PROB = 0.5


def random_walk(G: nx.Graph, test_index, steps=10) -> Any | None:
    start_node = str(list(G.nodes)[0])
    current_node = start_node
    actual_info = 0
    info_steps = []

    for i in range(steps):
        neighbors = list(G.neighbors(current_node))
        if len(neighbors) == 0:
            next_hop = random.choice(list(G.nodes))
            while next_hop == current_node:
                next_hop = random.choice(list(G.nodes))
        else:
            next_hop = random.choice(neighbors)
            while next_hop == current_node:
                next_hop = random.choice(neighbors)
        current_node = next_hop
        actual_info += G.nodes[current_node]['information'][test_index]
        info_steps.append(actual_info)
        G.nodes[current_node]['information'][test_index] = 0

    return info_steps


def ars_walk(G: nx.Graph, test_index, steps=10, tau=5) -> Any | None:
    if tau > steps:
        raise Exception("tau must be less than steps")

    current_node = str(list(G.nodes)[0])
    actual_info = 0
    info_steps = []
    t = 0

    for _ in range(steps):
        if t >= tau:
            current_node = random.choice(list(G.nodes))
        else:
            current_node = random.choice(list(G.neighbors(current_node)))

        info_to_add = G.nodes[current_node]['information'][test_index]

        if info_to_add > 0:
            t = 0
        else:
            t += 1

        actual_info += info_to_add
        info_steps.append(actual_info)
        G.nodes[current_node]['information'][test_index] = 0

    return info_steps


def pagerank_walk(G: nx.Graph, test_index, steps=10) -> Any | None:
    start_node = str(list(G.nodes)[0])
    current_node = start_node
    actual_info = 0
    info_steps = []

    for i in range(steps):
        coin_flip = np.random.rand()
        neighbors = list(G.neighbors(current_node))

        if coin_flip < PAGERANK_PROB or len(neighbors) == 0:
            next_hop = random.choice(list(G.nodes))
            while next_hop == current_node:
                next_hop = random.choice(list(G.nodes))
        else:
            next_hop = random.choice(list(neighbors))
            while next_hop == current_node:
                next_hop = random.choice(list(neighbors))

        if next_hop is None:
            return None

        current_node = next_hop
        actual_info += G.nodes[current_node]['information'][test_index]
        info_steps.append(actual_info)
        G.nodes[current_node]['information'][test_index] = 0

    return info_steps
