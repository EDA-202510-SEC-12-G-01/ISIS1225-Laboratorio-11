from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt

from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp

def new_graph(order):
    return {
        'vertices': mlp.new_map(order, 0.7),
        'num_edges': 0
    }

def insert_vertex(my_graph, key_u, info_u):
    v = vt.new_vertex(key_u, info_u)
    mlp.put(my_graph['vertices'], key_u, v)
    return my_graph

def update_vertex_info(my_graph, key_u, new_info_u):
    v = mlp.get(my_graph['vertices'], key_u)
    if v is None:
        return None
    vt.set_value(v, new_info_u)
    return my_graph

def remove_vertex(my_graph, key_u):
    v_remove = mlp.get(my_graph['vertices'], key_u)
    if v_remove is None:
        return None
    out_adj = vt.get_adjacents(v_remove)
    removed_out = mlp.size(out_adj)
    my_graph['num_edges'] -= removed_out
    vertices_keys = mlp.key_set(my_graph['vertices'])
    for i in range(al.size(vertices_keys)):
        u_key = al.get_element(vertices_keys, i)
        v = mlp.get(my_graph['vertices'], u_key)
        v_adjacents = vt.get_adjacents(v)
        if mlp.contains(v_adjacents, key_u):
            mlp.remove(v_adjacents, key_u)
            my_graph['num_edges'] -= 1
    mlp.remove(my_graph['vertices'], key_u)
    return my_graph

def add_edge(my_graph, key_u, key_v, weight=1.0):
    v_u = mlp.get(my_graph['vertices'], key_u)
    if v_u is None:
        raise Exception("El vertice u no existe")
    
    v_v = mlp.get(my_graph['vertices'], key_v)
    if v_v is None:
        raise Exception("El vertice v no existe")
    v_u_adjacents = vt.get_adjacents(v_u)
    had = mlp.contains(v_u_adjacents, key_v)
    edge = ed.new_edge(key_v, weight)
    mlp.put(v_u_adjacents, key_v, edge)
    if not had:
        my_graph['num_edges'] += 1
    return my_graph

def order(my_graph):
    return mlp.size(my_graph['vertices'])

def size(my_graph):
    return my_graph['num_edges']

def vertices(my_graph):
    lst = al.new_list()
    vertices_keys = mlp.key_set(my_graph['vertices'])
    for i in range(al.size(vertices_keys)):
        k = al.get_element(vertices_keys, i)
        al.add_last(lst, k)
    return lst

def degree(my_graph, key_u):
    v = mlp.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    return vt.degree(v)

def get_edge(my_graph, key_u, key_v):
    v_u = mlp.get(my_graph['vertices'], key_u)
    if v_u is None:
        raise Exception("El vertice u no existe")
    return vt.get_edge(v_u, key_v)

def get_vertex_information(my_graph, key_u):
    v = mlp.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    return vt.get_value(v)

def contains_vertex(my_graph, key_u):
    return mlp.contains(my_graph['vertices'], key_u)

def adjacents(my_graph, key_u):
    v = mlp.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    lst = al.new_list()
    v_adjacents = vt.get_adjacents(v)
    adjacents_keys = mlp.key_set(v_adjacents)
    for i in range(al.size(adjacents_keys)):
        k = al.get_element(adjacents_keys, i)
        al.add_last(lst, k)
    return lst

def edges_vertex(my_graph, key_u):
    v = mlp.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    
    lst = al.new_list()
    v_adjacents = vt.get_adjacents(v)
    adjacents_keys = mlp.key_set(v_adjacents)
    for i in range(al.size(adjacents_keys)):
        k = al.get_element(adjacents_keys, i)
        e = mlp.get(v_adjacents, k)
        al.add_last(lst, e)
    return lst

def get_vertex(my_graph, key_u):
    v = mlp.get(my_graph['vertices'], key_u)
    if v is None:
        raise Exception("El vertice no existe")
    return v