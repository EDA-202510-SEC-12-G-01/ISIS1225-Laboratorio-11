from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt

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



def new_graph(order):
    return {
        'vertices': mlp.new_map(order),
        'num_edges': 0
    }


def insert_vertex(my_graph, key_u, info_u):
    v = vt.new_vertex(key_u, info_u)
    mf.put(my_graph['vertices'], key_u, v)
    return my_graph


def update_vertex_info(my_graph, key_u, new_info_u):
    v = mf.get(my_graph['vertices'], key_u)
    if v is None:
        return None
    v.value = new_info_u
    return my_graph


def remove_vertex(my_graph, key_u):
    v_remove = mf.get(my_graph['vertices'], key_u)
    if v_remove is None:
        return None
    out_adj = v_remove.adjacents
    removed_out = mf.size(out_adj)
    my_graph['num_edges'] -= removed_out
    for u_key in mf.key_set(my_graph['vertices']):
        v = mf.get(my_graph['vertices'], u_key)
        if mf.contains_key(v.adjacents, key_u):
            mf.remove(v.adjacents, key_u)
            my_graph['num_edges'] -= 1
    mf.remove(my_graph['vertices'], key_u)
    return my_graph


def add_edge(my_graph, key_u, key_v, weight=1.0):
    v_u = mf.get(my_graph['vertices'], key_u)
    if v_u is None:
        raise Exception("El vertice u no existe")
    v_v = mf.get(my_graph['vertices'], key_v)
    if v_v is None:
        raise Exception("El vertice v no existe")
    had = mf.contains_key(v_u.adjacents, key_v)
    edge = ed.new_edge(key_v, weight)
    mf.put(v_u.adjacents, key_v, edge)
    if not had:
        my_graph['num_edges'] += 1
    return my_graph


def order(my_graph):
    return mf.size(my_graph['vertices'])


def size(my_graph):
    return my_graph['num_edges']


def vertices(my_graph):
    lst = al.new_array_list()
    for k in mf.key_set(my_graph['vertices']):
        lst.add(k)
    return lst


def degree(my_graph, key_u):
    v = mf.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    return mf.size(v.adjacents)


def get_edge(my_graph, key_u, key_v):
    v_u = mf.get(my_graph['vertices'], key_u)
    if v_u is None:
        raise Exception("El vertice u no existe")
    return mf.get(v_u.adjacents, key_v)


def get_vertex_information(my_graph, key_u):
    v = mf.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    return v.value


def contains_vertex(my_graph, key_u):
    return mf.contains_key(my_graph['vertices'], key_u)


def adjacents(my_graph, key_u):
    v = mf.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    lst = al.new_array_list()
    for k in mf.key_set(v.adjacents):
        lst.add(k)
    return lst


def edges_vertex(my_graph, key_u):
    v = mf.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    lst = al.new_array_list()
    for k in mf.key_set(v.adjacents):
        e = mf.get(v.adjacents, k)
        lst.add(e)
    return lst


def get_vertex(my_graph, key_u):
    v = mf.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    return v