from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import diagraph as G


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

def bfs(my_graph, source):
    if not G.contains_vertex(my_graph, source):
        raise Exception("El vertice source no existe")
    marked = mf.new_map(G.order(my_graph))
    edge_to = mf.new_map(G.order(my_graph))
    queue = q.new_queue()

    mf.put(marked, source, True)
    queue.enqueue(source)

    while not queue.is_empty():
        v = queue.dequeue()
        for w in G.adjacents(my_graph, v).elements:
            if not mf.contains_key(marked, w) or mf.get(marked, w) is None:
                mf.put(marked, w, True)
                mf.put(edge_to, w, v)
                queue.enqueue(w)
    return {
        'edge_to': edge_to,
        'marked': marked
    }


def has_path_to_bfs(search, key_v):
    marked = search['marked']
    return mf.contains_key(marked, key_v) and mf.get(marked, key_v) is True


def path_to_bfs(search, key_v):
    if not has_path_to_bfs(search, key_v):
        return None
    path = s.new_stack()
    edge_to = search['edge_to']
    v = key_v
    while mf.contains_key(edge_to, v) and mf.get(edge_to, v) is not None:
        path.push(v)
        v = mf.get(edge_to, v)
    path.push(v)
    return path