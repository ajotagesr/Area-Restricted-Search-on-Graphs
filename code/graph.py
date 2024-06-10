from math import trunc
import networkx as nx
import random
import cluster_erdos as ce

INTRACLUSTER_EDGE_PROB = 0.65
INTERCLUSTER_EDGE_PROB = 0.15



def truncate_float(float_number, decimal_places):
    multiplier = 10 ** decimal_places
    return int(float_number * multiplier) / multiplier


def graph_with_clusters(n_clusters=5, n_nodes=40, n_tests=5, perc=None) -> nx.Graph:
    if n_nodes < n_clusters:
        raise Exception("n_nodes must be greater than n_clusters")

    nodes = [str(i + 1) for i in range(n_nodes)]
    G = nx.Graph()
    # G = nx.DiGraph()
    G.add_nodes_from(nodes)

    G.graph['n_clusters'] = n_clusters
    G.graph['n_nodes'] = n_nodes
    G.graph['n_tests'] = n_tests

    cluster_list = create_subgroups(nodes, n_clusters)

    # add intra-cluster edges
    for index, cluster in enumerate(cluster_list):
        for node in cluster:
            G.nodes[node]['cluster'] = index + 1

        intra_cluster_edges = []
        for node1 in cluster:
            for node2 in cluster:
                if node1 != node2 and random.random() < INTRACLUSTER_EDGE_PROB:
                    intra_cluster_edges.append((node1, node2))
        intra_cluster_edges = list(set(intra_cluster_edges))
        G.add_edges_from(intra_cluster_edges)

    # add inter-cluster edges
    inter_cluster_edges = []
    for i in range(n_clusters):
        for cluster1 in cluster_list:
            for cluster2 in cluster_list:
                if cluster1 != cluster2 and random.random() < INTERCLUSTER_EDGE_PROB:
                    inter_cluster_edges.append((random.choice(cluster1), random.choice(cluster2)))
    inter_cluster_edges = list(set(inter_cluster_edges))
    G.add_edges_from(inter_cluster_edges)

    # randomly select half of the clusters to have no information
    if perc is None:
        clusters_with_info = random.sample(range(1, n_clusters + 1), n_clusters // 2)
    else:
        clusters_with_info = random.sample(range(1, n_clusters + 1), int(n_clusters * perc))

    total_information = 0

    for node in G.nodes:
        info = random.random() if G.nodes[node]['cluster'] in clusters_with_info else 0
        G.nodes[node]['information'] = []
        G.nodes[node]['colour'] = 'green' if info > 0 else 'red'
        for _ in range(n_tests):
            G.nodes[node]['information'].append(info)
        total_information += info

    G.graph['total_information'] = total_information

    return G


def graph_erdos(n_clusters=10, avgcl=20, mc=5, mi=2, n_tests=5) -> nx.Graph:
    erdos_graph = ce.g_make(n_clusters, avgcl, mc, mi)

    n_nodes = len(erdos_graph)

    G = nx.Graph()

    G.graph['n_clusters'] = n_clusters
    G.graph['n_nodes'] = n_nodes
    G.graph['n_tests'] = n_tests

    nodes = [str(i) for i in range(n_nodes)]
    G.add_nodes_from(nodes)

    for index, (cl, outlinks) in enumerate(erdos_graph):
        node = nodes[index]
        G.nodes[node]['cluster'] = cl
        for dest in outlinks:
            if node != str(dest):
                G.add_edge(node, str(dest))

    G.graph['total_information'] = 0

    return G


def modify_graph_information(G: nx.Graph, perc: float) -> nx.Graph:
    for node in G.nodes:
        G.nodes[node]['information'] = []

    clusters_with_info = random.sample(range(G.graph['n_clusters']), int(G.graph['n_clusters'] * perc))
    # print(perc, clusters_with_info)

    total_information = 0

    for node in G.nodes:
        info = random.random() if G.nodes[node]['cluster'] in clusters_with_info else 0
        for _ in range(G.graph['n_tests']):
            G.nodes[node]['information'].append(info)
        total_information += info
        G.nodes[node]['colour'] = 'green' if info > 0 else 'red'

    G.graph['total_information'] = total_information

    return G


def graph_add_information(G: nx.Graph, perc: float, prev_clusters=None, previous_perc=0) -> nx.Graph:
    if prev_clusters is None or previous_perc == 0:
        prev_clusters = []

    previous_perc = truncate_float(previous_perc, 2)

    perc_to_add = perc - previous_perc
    # round up
    perc_to_add = round(perc_to_add, 2)
    clusters = list(range(G.graph['n_clusters']))

    selectable_clusters = [c for c in clusters if c not in prev_clusters]
    clusters_with_info = prev_clusters + random.sample(selectable_clusters, int(G.graph['n_clusters'] * perc_to_add))

    if perc == 1:
        clusters_with_info = clusters
    
    total_information = 0
    
    for node in G.nodes:
        info = random.random() if G.nodes[node]['cluster'] in clusters_with_info else 0
        
        if 'information' not in G.nodes[node]:
            G.nodes[node]['information'] = [info] * G.graph['n_tests']
        else:
            info = G.nodes[node]['information'][0]
        
        total_information += info
        G.nodes[node]['colour'] = 'green' if info > 0 else 'red'
        
    G.graph['total_information'] = total_information
    
    return G, clusters_with_info



def graph_get_total_information(G: nx.Graph, test_index=0) -> float:
    total_information = 0
    for node in G.nodes:
        info = G.nodes[node]['information'][test_index]
        total_information += info
    return total_information


def create_subgroups(node_list, n_subgroups):
    """
    Create the communities of the graph.

    Args:
        node_list (list): List of nodes in the graph.
        n_subgroups (int): Number of communities to create.

    Returns:
        list: List of lists, each list containing the nodes of a community.
    """
    subgroup_sizes = []

    # at least one node per subgroup
    for i in range(n_subgroups):
        subgroup_sizes.append(1)

    # distribute the rest of the nodes
    while sum(subgroup_sizes) != len(node_list):
        subgroup_sizes[random.randint(0, n_subgroups - 1)] += 1

    # create the subgroups
    subgroups = []
    for i in range(n_subgroups):
        subgroup = []
        for j in range(subgroup_sizes[i]):
            node_name_position = sum(subgroup_sizes[0:i]) + j
            subgroup.append(node_list[node_name_position])
        subgroups.append(subgroup)

    return subgroups
