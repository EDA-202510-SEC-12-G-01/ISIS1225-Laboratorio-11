from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import diagraph as G
from DataStructures.Graph import bfs as bfs
from DataStructures.Graph import dfs as dfs
from DataStructures.Graph import prim as prim


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


def dijkstra(my_graph, source):
    if not G.contains_vertex(my_graph, source):
        raise Exception("El vertice source no existe")
    dist_to = mf.new_map(G.order(my_graph))
    edge_to = mf.new_map(G.order(my_graph))
    marked = mf.new_map(G.order(my_graph))
    ipq = pq.new_priority_queue(G.order(my_graph))

    for v in mf.key_set(my_graph['vertices']):
        mf.put(dist_to, v, float('inf'))
    mf.put(dist_to, source, 0.0)
    pq.insert(ipq, source, 0.0)

    while not pq.is_empty(ipq):
        v = pq.del_min(ipq)
        mf.put(marked, v, True)
        for w in G.adjacents(my_graph, v).elements:
            e = G.get_edge(my_graph, v, w)
            wt = e.weight
            if mf.get(dist_to, v) + wt < mf.get(dist_to, w):
                mf.put(dist_to, w, mf.get(dist_to, v) + wt)
                mf.put(edge_to, w, v)
                if pq.contains(ipq, w):
                    pq.decrease_key(ipq, w, mf.get(dist_to, w))
                else:
                    pq.insert(ipq, w, mf.get(dist_to, w))
    return {'dist_to': dist_to, 'edge_to': edge_to, 'marked': marked}


def dist_to(key_v, dijkstra_search):
    if not mf.contains_key(dijkstra_search['dist_to'], key_v):
        raise Exception("El vertice no existe o Dijkstra no ejecutado")
    return mf.get(dijkstra_search['dist_to'], key_v)


def has_path_to(key_v, dijkstra_search):
    return mf.contains_key(dijkstra_search['dist_to'], key_v) and dijkstra_search['dist_to'][key_v] < float('inf')


def path_to(key_v, dijkstra_search):
    if not has_path_to(key_v, dijkstra_search):
        return None
    path = s.new_stack()
    v = key_v
    while mf.contains_key(dijkstra_search['edge_to'], v) and mf.get(dijkstra_search['edge_to'], v) is not None:
        path.push(v)
        v = mf.get(dijkstra_search['edge_to'], v)
    path.push(v)
    return path
