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

def dfo(my_graph):
    marked = mf.new_map(G.order(my_graph))
    pre = al.new_array_list()
    post = al.new_array_list()
    reversepost = s.new_stack()
    aux = {
        'marked': marked,
        'pre': pre,
        'post': post,
        'reversepost': reversepost
    }
    def dfs_vertex(my_graph, v_key, aux):
        mf.put(aux['marked'], v_key, True)
        aux['pre'].add(v_key)
        for w in G.adjacents(my_graph, v_key).elements:
            if not mf.contains_key(aux['marked'], w) or mf.get(aux['marked'], w) is None:
                dfs_vertex(my_graph, w, aux)
        aux['post'].add(v_key)
        aux['reversepost'].push(v_key)
    for v_key in mf.key_set(my_graph['vertices']):
        if not mf.contains_key(marked, v_key) or mf.get(marked, v_key) is None:
            dfs_vertex(my_graph, v_key, aux)

    return aux