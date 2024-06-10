import os
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import datetime

PLOTS_PATH = 'plots/'
ARS_STEPS_PATH = PLOTS_PATH + 'ars_steps/'
ARS_STEPS_PERC_CLUSTERS_PATH = PLOTS_PATH + 'ars_steps_perc_clusters/'

FONTSIZE = 9
COLOR_LIST = ['green', 'yellow', 'orange', 'pink', 'red', 'gray', 'purple', 'blue', 'brown', 'cyan', 'magenta']
SUBTEXT_FONT_SIZE = 7

methods = {
    '1': 'Random Walk',
    '2': 'ARS',
    '3': 'PageRank'
}


def plot_graph(G):
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=150, node_color="skyblue", font_size=FONTSIZE, font_weight="bold")
    plt.title('Clustered Graph')
    plt.show()

def plot_erdos_graph(G, n, p):
    # pos = nx.kamada_kawai_layout(G)
    pos = nx.circular_layout(G)
    # add contour to the nodes
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=20, font_weight="bold")
    
    plt.title('Grafo ER con N = ' + str(n) + ' y p = ' + str(p))

def plot_graph_colored(G):
    if G.graph['n_clusters'] > len(COLOR_LIST):
        print("Too many clusters to plot with different colors, using default color")
        plot_graph(G)
        return
    node_colors = [COLOR_LIST[G.nodes[node]['cluster']] for node in G.nodes]
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=False, node_size=70, font_size=FONTSIZE, font_weight="bold", node_color=node_colors)
    # plt.title('Clustered Graph')
    plt.show()


def plot_graph_colored_by_info(G, perc=None):
    node_colors = [G.nodes[node]['colour'] for node in G.nodes]
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=False, node_size=70, font_size=FONTSIZE, font_weight="bold", node_color=node_colors)

    if perc is not None:
        plt.title('Clustered Graph with information in ' + str(perc*100) + '% of clusters')
    else:
        plt.title('Clustered Graph with information')

    legend_labels = {'Green': 'Information', 'Red': 'No Information'}
    for color, description in legend_labels.items():
        plt.scatter([], [], c=color, label=description)

    plt.legend(scatterpoints=1, labelspacing=1)
    plt.show()


def plot_information_gained_by_step(random_walk_info, total_info):
    plt.plot(random_walk_info)
    plt.ylim(0, total_info)
    plt.title('Information gained Random Walk')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.show()


def plot_information_gained_by_step_ars(ars_info, total_info):
    plt.plot(ars_info)
    plt.ylim(0, total_info)
    plt.title('Information gained ARS')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.show()


def plot_information_gained_by_step_pagerank(pagerank_info, total_info):
    plt.plot(pagerank_info)
    plt.ylim(0, total_info)
    plt.title('Information gained PageRank')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.show()


def plot_information_gained_by_step_random_walk_and_ars(random_walk_info, ars_info, total_info):
    plt.plot(random_walk_info, label='Random Walk')
    plt.plot(ars_info, label='ARS')
    plt.ylim(0, total_info)
    plt.title('Random Walk VS ARS')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.legend()
    plt.show()


def plot_information_gained_by_step_pagerank_and_ars(pagerank_info, ars_info, total_info):
    plt.plot(pagerank_info, label='PageRank')
    plt.plot(ars_info, label='ARS')
    plt.ylim(0, total_info)
    plt.title('PageRank VS ARS')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.legend()
    plt.show()


def plot_mean(info_list, total_info, method):
    mean_info = np.mean(info_list, axis=0)
    plt.plot(mean_info)
    plt.ylim(0, total_info)
    plt.title(f'Mean Information gained {method}')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.show()


def plot_variance(info_list, method):
    variance_info = np.var(info_list, axis=0)
    plt.plot(variance_info)
    plt.title(f'Variance Information gained {method}')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.show()


def plot_std(info_list, method):
    std_info = np.std(info_list, axis=0)
    plt.plot(std_info)
    plt.title(f'Standard Deviation Information gained {method}')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.show()


def plot_stats(info_list, total_info, method):
    plot_mean(info_list, total_info, method)
    plot_variance(info_list, method)
    plot_std(info_list, method)


def plot_2methods(info_list1, info_list2, total_info, method1, method2):
    mean_info1 = np.mean(info_list1, axis=0)
    mean_info2 = np.mean(info_list2, axis=0)
    plt.plot(mean_info1, label=method1)
    plt.plot(mean_info2, label=method2)
    plt.ylim(0, total_info)
    plt.title(f'Mean Information gained {method1} VS {method2}')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.legend()
    plt.savefig(PLOTS_PATH + f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_mean_{method1}_{method2}_.jpg')
    plt.show()

    var_info1 = np.var(info_list1, axis=0)
    var_info2 = np.var(info_list2, axis=0)
    plt.plot(var_info1, label=method1)
    plt.plot(var_info2, label=method2)
    plt.title(f'Variance Information gained {method1} VS {method2}')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.legend()
    plt.savefig(PLOTS_PATH + f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_var_{method1}_{method2}_.jpg')
    plt.show()

    std_info1 = np.std(info_list1, axis=0)
    std_info2 = np.std(info_list2, axis=0)
    plt.plot(std_info1, label=method1)
    plt.plot(std_info2, label=method2)
    plt.title(f'Standard Deviation Information gained {method1} VS {method2}')
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.legend()
    plt.savefig(PLOTS_PATH + f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_std_{method1}_{method2}_.jpg')
    plt.show()


def plot_3methods(simulation_parameters, info_list1, info_list2, info_list3, total_info, method1, method2, method3):
    n_clusters, n_nodes, n_tests = simulation_parameters
    dir_path = PLOTS_PATH + "3-methods/" + str(n_clusters) + "-clusters/"
    os.makedirs(dir_path, exist_ok=True)
    dir_path = dir_path + str(n_nodes) + "-nodes/"
    os.makedirs(dir_path, exist_ok=True)

    mean_info1, mean_info2, mean_info3 = np.mean(info_list1, axis=0), np.mean(info_list2, axis=0), np.mean(info_list3,
                                                                                                   axis=0)
    plt.figure()
    plt.plot(mean_info1, label=method1)
    plt.plot(mean_info2, label=method2)
    plt.plot(mean_info3, label=method3)
    # plt.ylim(0, total_info)
    plt.title('Mean Information gained by method')
    plt.xlabel('Steps')
    plt.ylabel('Information')
    plt.legend()
    plt.savefig(dir_path + f'mean.jpg')
    # plt.show()
    plt.close()

    total_infos = (mean_info1[-1], mean_info2[-1], mean_info3[-1])
    methods = (method1, method2, method3)
    plot_total_info_3methods(simulation_parameters, total_infos, methods)

    var_info1, var_info2, var_info3 = np.var(info_list1, axis=0), np.var(info_list2, axis=0), np.var(info_list3, axis=0)
    plt.figure()
    plt.plot(var_info1, label=method1)
    plt.plot(var_info2, label=method2)
    plt.plot(var_info3, label=method3)
    plt.title('Variance of Information gained by method')
    plt.xlabel('Steps')
    plt.ylabel('Information')
    plt.legend()
    plt.savefig(dir_path + f'var.jpg')
    # plt.show()
    plt.close()

    std_info1, std_info2, std_info3 = np.std(info_list1, axis=0), np.std(info_list2, axis=0), np.std(info_list3, axis=0)
    plt.figure()
    plt.plot(std_info1, label=method1)
    plt.plot(std_info2, label=method2)
    plt.plot(std_info3, label=method3)
    plt.title('Standard Deviation of Information gained by method')
    plt.xlabel('Steps')
    plt.ylabel('Information')
    plt.legend()
    plt.savefig(dir_path + f'std.jpg')
    # plt.show()
    plt.close()


def plot_total_info_3methods(simulation_parameters, total_infos, methods):    
    n_clusters, n_nodes, _ = simulation_parameters
    dir_path = PLOTS_PATH + "3-methods/" + str(n_clusters) + "-clusters/"
    os.makedirs(dir_path, exist_ok=True)
    dir_path = dir_path + str(n_nodes) + "-nodes/"
    os.makedirs(dir_path, exist_ok=True)

    plt.figure()
    plt.bar(methods, total_infos)
    plt.xlabel('Método')
    plt.ylabel('Información')
    plt.title('Información total obtenida por método')
    plt.savefig(dir_path + f'total_info.jpg')
    plt.close()



def plot_ars_by_steps_to_jump(simulation_parameters, ars_steps_results_dict):
    n_clusters, n_nodes, n_tests = simulation_parameters
    dir_path = ARS_STEPS_PATH + str(n_clusters) + "-clusters/" + str(n_nodes) + "-nodes/"
    os.makedirs(dir_path, exist_ok=True)
    dir_path = dir_path + str(n_nodes) + "-nodes/"
    os.makedirs(dir_path, exist_ok=True)

    for step, results in ars_steps_results_dict.items():
        plt.plot(results, label=f'{step} steps')

    plt.title(f'ARS by Steps to Jump')
    plt.text(0, -0.2, f'Clusters: {n_clusters}, Nodes: {n_nodes}, Tests: {n_tests}', fontsize=SUBTEXT_FONT_SIZE,
             transform=plt.gca().transAxes)
    plt.xlabel('Time step')
    plt.ylabel('Information')
    plt.legend()
    plt.savefig(
        dir_path + f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_ars_steps_{n_clusters}_{n_nodes}_{n_tests}_.jpg')
    plt.show()


def plot_ars_by_steps_to_jump_and_perc_cl_info(simulation_parameters, ars_results, steps_to_plot):
    n_clusters, n_nodes, n_tests = simulation_parameters
    dir_path = ARS_STEPS_PERC_CLUSTERS_PATH + str(n_clusters) + "-clusters/"
    os.makedirs(dir_path, exist_ok=True)
    dir_path = dir_path + str(n_nodes) + "-nodes/"
    os.makedirs(dir_path, exist_ok=True)
    for perc in ars_results.keys():
        plt.figure()
        for steps, results in ars_results[perc].items():
            if steps in steps_to_plot:
                plt.plot(results, label=f'Tau: {steps}')
        plt.title(f'ARS: Multiple Tau and {perc*100}% of clusters with info')
        plt.title(f'{perc*100}% of clusters with information')
        plt.suptitle(f'Clusters: {n_clusters}, Nodes: {n_nodes}, Tests: {n_tests}')
        plt.xlabel('Steps')
        plt.ylabel('Information')
        plt.legend()
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        save_path = dir_path + f'ARSTAU{int(perc * 1000)}.jpg'
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()


def plot_ars_by_steps_to_jump_and_perc_cl_info_no_legend(simulation_parameters, ars_results, steps_to_plot):
    n_clusters, n_nodes, n_tests = simulation_parameters
    dir_path = ARS_STEPS_PERC_CLUSTERS_PATH + str(n_clusters) + "-clusters/"
    os.makedirs(dir_path, exist_ok=True)
    dir_path = dir_path + str(n_nodes) + "-nodes/"
    os.makedirs(dir_path, exist_ok=True)
    for perc in ars_results.keys():
        plt.figure()
        for steps, results in ars_results[perc].items():
            if steps in steps_to_plot:
                plt.plot(results)
        plt.title(f'{perc*100}% of clusters with information')
        plt.xlabel('Steps')
        plt.ylabel('Information')
        plt.legend().remove()
        save_path = dir_path + f'ZARSTAU{int(perc * 1000)}.jpg'
        plt.savefig(save_path, bbox_inches='tight')
        plt.close()


def plot_total_information_gained_by_steps_and_perc_cl_info(simulation_parameters, ars_results):
    n_clusters, n_nodes, n_tests = simulation_parameters
    dir_path = ARS_STEPS_PERC_CLUSTERS_PATH + str(n_clusters) + "-clusters/" + str(n_nodes) + "-nodes/" + "total_info/"
    os.makedirs(dir_path, exist_ok=True)

    for perc in ars_results.keys():
        plt.figure()

        total_info_dict = {}
        for steps, results in ars_results[perc].items():
            total_info_dict[steps] = results[-1]

        # Extract keys and values for plotting
        x_values = list(total_info_dict.keys())
        y_values = list(total_info_dict.values())
        plt.plot(x_values, y_values)
        # plt.scatter(x_values, y_values)
        plt.title(f'Information gained in a graph with {perc*100}% of clusters with information')
        # plt.title(f'{perc*100}% of clusters with information')
        plt.suptitle(f'Clusters: {n_clusters}, Nodes: {n_nodes}, Tests: {n_tests}')
        plt.xlabel('Tau')
        plt.ylabel('Total Information')
        save_path = dir_path + f'{int(perc * 1000)}TOTALINFO.jpg'
        plt.savefig(save_path)
        plt.close()


def plot_info_by_steps_and_steps_taken(simulation_parameters, ars_results):
    n_clusters, n_nodes, n_tests = simulation_parameters
    dir_path = ARS_STEPS_PATH + str(n_clusters) + "-clusters/" + str(n_nodes) + "-nodes/" + "info_by_steps/"
    os.makedirs(dir_path, exist_ok=True)
    
    for perc in ars_results.keys():
        plt.figure()
        steps = list(ars_results[perc].keys())
        info = list(ars_results[perc].values())


def plot_all_percs_in_one(simulation_parameters, ars_results):
    n_clusters, n_nodes, n_tests = simulation_parameters
    dir_path = ARS_STEPS_PERC_CLUSTERS_PATH + str(n_clusters) + "-clusters/" + str(n_nodes) + "-nodes/" + "total_info/"
    os.makedirs(dir_path, exist_ok=True)
    
    plt.figure()
    total_info_dict = {}
    for perc in ars_results.keys():
        for steps, results in ars_results[perc].items():
            total_info_dict[steps] = results[-1]
        x_values = list(total_info_dict.keys())
        y_values = list(total_info_dict.values())
        plt.plot(x_values, y_values, label=f'{perc*100}%')
    plt.title(f'Total Information gained by TAU and percentage of clusters with information')
    plt.suptitle(f'Clusters: {n_clusters}, Nodes: {n_nodes}, Tests: {n_tests}')
    plt.xlabel('Tau de ARS')
    plt.ylabel('Información total')
    plt.legend()
    save_path = dir_path + f'ALLINONE.jpg'
    plt.savefig(save_path)
    plt.close()
