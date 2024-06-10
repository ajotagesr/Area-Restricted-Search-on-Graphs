#
#   Generating a graph with a community structure. Each community is an
#   Erdos random graph, and the communities are joined in an
#   Erdos-like way (with a different connection parameter, of course)
#
#
import sys
import random

#
#  g = erdos_make(n, m, c)
#  
#
# Builds an Erdos graph given the number of nodes, the average degree
# parameters, and the cluster number to be assigned to the nodes of
# the graph
#
# 
# Parameters:
# n:   number of nodes in the graph
# m:   average degree of a node of the graph
# c:   cluster number to be assigned to the nodes of the graph
#
# Returns: a list of pair:
#
#  [[c, adj0], [c, adj1],...., [c, adjn]]
#
#  here c is the cluster number of the node (the same for all), and
#  adj is a list of node indices to which the node is connected. The
#  id of a node is given implicitly by its position on the list
#  (element g[k] is the element of the node with identifier k)
#
#  NOTE: There is no guarantee that the graph is connected, especially
#  for small m. If a connected graph is needed, some additional
#  measures must be taken
#
def erdos_make(n, m, c):
    adj = [[] for _ in range(n)]
    edgeno = n*m
    for _ in range(edgeno):
        src = random.randint(0,n-1)
        dst = random.randint(0,n-1)
        w = 0
        while (src == dst) or (dst in adj[src]):
            src = random.randint(0,n-1)
            dst = random.randint(0,n-1)
            w += 1
            if w > 10000:     # Too many attempts. Give up
                return [[c, a] for a in adj]

        adj[src] += [dst]
        adj[dst] += [src]

    return [[c, a] for a in adj]


#
# g = g_join(g1, g2)
#
# Joins two graphs, both in the format returned by erdos_make. The
# indices of the second graph will be those following those of the
# first, and the indices of the adjacency list will be changed
# accordingly
#
# NOTE: the parameters will be affected. If you need them unchanged,
# make a copy
#
#
def g_join(g1, g2):
    base = len(g1)
    for u in range(len(g2)):
        for k in range(len(g2[u][1])):
            g2[u][1][k] += base
    g = g1 + g2
    return g


#
#  g = g_clst_edge(g, clst, c1, c2)
#
#  Creates an edge between a random node of cluster c1 and a random
#  node of cluster c2
#
#  Parameters
#
#  g:    the graph to which the edge is addes
#  clst: cluster counter. List of pairs (a,b): nodes of cluster k are
#        in the range clst[k][0] to clst[k][1]
#  c1:   first cluster to be joined
#  c2:   second cluster to be joined
#
#  Returns:
#    the graph g with the edge added (the parameter is changed: this
#    is not a copy)
#
def g_clst_edge(g, clst, c1, c2):
    src = random.randint(clst[c1][0],clst[c1][1]-1)
    dst = random.randint(clst[c2][0],clst[c2][1]-1)
    w = 0
    while (src == dst) or (dst in g[src][1]):
        src = random.randint(clst[c1][0],clst[c1][1]-1)
        dst = random.randint(clst[c2][0],clst[c2][1]-1)
        
        w += 1
        if w > 10000:     # Too many attempts. Give up
            return g

    g[src][1] += [dst]
    g[dst][1] += [src]

    return g
    

#
#  Disjoint set structure. Creates a new one with n sets
#
def ds_make(n):
    return n*[-1]

#
#  Finds the representative of an element
#  (no path compression)
#
def ds_find(ds, n):
    while ds[n] >= 0:
        n = ds[n]
    return n


#
# Union of the sets representatives of two element. Returns the
# representative of the union
#
def ds_union(ds, a, b):
    x = ds_find(ds, a)
    y = ds_find(ds, b)
    if x == y:
        return x
    if ds[y] < ds[x]:
        ds[x] = y
        return y
    elif ds[x] < ds[y]:
        ds[y] = x
        return x
    else:
        ds[y] = x
        ds[x] -= 1
        return x


#
#  g = g_fix(g)
#
#  Fixes a graph making it connected. Finds the connected components
#  and, if there is more than one, draws a single edge from a node in
#  the first to one in the second.
#
#  Parameters:
#  g:    the graph to fix, in the format returned by erdos_make
#
#  Returns: 
#     The graph g, which has been changed by (possibly) adding
#     edges
#
def g_fix(g):
    ds = ds_make(len(g))
    for u in range(len(g)):
        for v in g[u][1]:
            ds_union(ds, u, v)
    p = -1
    c = -1
    for k in range(len(ds)):
        if ds[k] < 0:
            if c < 0:
                c = k
            else:
                p = c
                c = k
                g[p][1] += [c]
                g[c][1] += [p]
    return g


#
#  Creates a clusters graph. The graph is constructed by first
#  creating n disconnected clusters, each one of which is an erdos
#  graph with the prescribed connectivity. The cluster size if a rando
#  variable with exponential distribution (and minimum size of 2, to
#  avoid empty clusters). Corrections are intruduced to make sure that
#  each cluster is fully connected.
#
#  Then the clusters are connected by drawing edges from a random node
#  of a cluster to a random node of another one. The clusters are
#  threaded in an erdos-like fashion with a different connection
#  parameters. Here too there is a small correction (edges added)
#  inserted to make sure that the final graph is connected
#
#  Parameters
#
#    cno      Number of clusters
#    clave    average sze of each cluster
#    mc       average degree of the nodes of a cluster
#    mi       average degree between clusters
#
#  Returns
#
#  A graph structure, which is a list of pairs:
#
#  [[c, adj0], [c, adj1],...., [c, adjn]]
#
#  here c is the cluster number of the node, and adj is a list of node
#  indices to which the node is connected. The id of a node is given
#  implicitly by its position on the list (element g[k] is the element
#  of the node with identifier k)
#
def g_make(cno, clave, mc, mi):
    clst = [[] for _ in range(cno)]   # List of pairs (a,b): nodes of cluster k are in the range clst[k][0] to clst[k][1]
    clst[-1] = [0,0]                  # This is  a trick to initialize properly the element 0 in the loop
    #                                                                                                  |
    #                                                                                                  |
    #  Creates the graph composed of c independent components, each one of them being a connected      |
    #  Erdos graph (with correction)                                                                   |
    g = []                                                       #                                     |
    for cq in range(cno):                                        #                                     |
        size = 2 + int(random.expovariate(1.0/float(clave)))     #                                     V
        clst[cq] = [clst[cq-1][1], clst[cq-1][1]+size]     #  See? When cq=0 and cq-1=-1 I use the trick above
        # print(clst[cq])
        g1 = erdos_make(size, mc, cq)
        g_fix(g1)
        g = g_join(g, g1)

    # Thread the clusters. Keep track of which clusters are connected
    # using a disjoint sets structure
    clds = ds_make(cno)
    nedge = cno*mi

    for k in range(nedge):
        cl1 = random.randint(0,cno-1)
        cl2 = random.randint(0,cno-1)
        g_clst_edge(g, clst, cl1, cl2)       
        ds_union(clds, cl1, cl2)

    # Now connect with an edge the parts that have remained disconnected
    p = -1
    c = -1
    for k in range(len(clds)):
        if clds[k] < 0:
            if c < 0:
                c = k
            else:
                p = c
                c = k
                g_clst_edge(g, clst, p, c)       
    return g



#
#  Testing script
#

# if __name__ == "__main__":
#     cno = 5    #  Number of clusters
#     clave = 10  # average sze of each cluster
#     mc = 5      # average degree of the nodes of a cluster
#     mi = 2      # average degree between clusters

#     g = g_make(cno, clave, mc, mi)
    
#     for q in g:
#         print(q)

#     print(len(g))
