from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import diagraph as G
from DataStructures.Graph import bfs as bfs
from DataStructures.Graph import dfs as dfs

from DataStructures.List import array_list as al
from DataStructures.List import list_iterator as li
from DataStructures.List import list_node as ld
from DataStructures.List import single_linked_list as sll

from DataStructures.Map import map_entry as me
from DataStructures.Map import map_funtions as mf
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Map import map_separate_chaining as msc

from DataStructures.Priority_queue import index_pq_entry as ipe
from DataStructures.Priority_queue import priority_queue as pq

from DataStructures.Queue import queue as q

from DataStructures.Stack import stack as s

from DataStructures.Tree import bst_node as bn
from DataStructures.Tree import rbt_node as rb
from DataStructures.Tree import red_black_tree as rbt


def prim_mst(my_graph, source):
    marked = mf.new_map(G.order(my_graph))
    edge_to = mf.new_map(G.order(my_graph))
    dist_to = mf.new_map(G.order(my_graph))
    ipq = pq.new_priority_queue(G.order(my_graph))

    for v in mf.key_set(my_graph['vertices']):
        mf.put(dist_to, v, float('inf'))
    if not G.contains_vertex(my_graph, source):
        raise Exception("El vertice source no existe")
    mf.put(dist_to, source, 0.0)
    pq.insert(ipq, source, 0.0)

    while not pq.is_empty(ipq):
        v = pq.del_min(ipq)
        mf.put(marked, v, True)
        for w in G.adjacents(my_graph, v).elements:
            e = G.get_edge(my_graph, v, w)
            wt = e.weight
            if not mf.contains_key(marked, w):
                if wt < mf.get(dist_to, w):
                    mf.put(dist_to, w, wt)
                    mf.put(edge_to, w, v)
                    if pq.contains(ipq, w):
                        pq.decrease_key(ipq, w, wt)
                    else:
                        pq.insert(ipq, w, wt)
    return {'marked': marked, 'edge_to': edge_to, 'dist_to': dist_to}


def edges_mst(my_graph, prim_search):
    if 'edge_to' not in prim_search:
        raise Exception("Prim no ejecutado")
    qres = q.new_queue()
    for v in mf.key_set(prim_search['edge_to']):
        u = mf.get(prim_search['edge_to'], v)
        if u is not None:
            e = ed.new_edge(v, G.get_edge(my_graph, u, v).weight)
            q.enqueue(qres, (u, v, e.weight))
    return qres


def weight_mst(my_graph, prim_search):
    total = 0.0
    for v in mf.key_set(prim_search['edge_to']):
        u = mf.get(prim_search['edge_to'], v)
        if u is not None:
            total += G.get_edge(my_graph, u, v).weight
    return total