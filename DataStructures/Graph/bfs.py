from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import diagraph as G

from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as s

def bfs(my_graph, source):
    if not G.contains_vertex(my_graph, source):
        raise Exception("El vertice source no existe")
    marked = mlp.new_map(G.order(my_graph), 0.7)
    edge_to = mlp.new_map(G.order(my_graph), 0.7)
    queue = q.new_queue()
    mlp.put(marked, source, True)
    q.enqueue(queue, source)

    while not q.is_empty(queue):
        v = q.dequeue(queue)
        adjacents_list = G.adjacents(my_graph, v)
        for i in range(al.size(adjacents_list)):
            w = al.get_element(adjacents_list, i)
            if not mlp.contains(marked, w) or mlp.get(marked, w) is None:
                mlp.put(marked, w, True)
                mlp.put(edge_to, w, v)
                q.enqueue(queue, w)
    return {
        'edge_to': edge_to,
        'marked': marked
    }

def has_path_to_bfs(search, key_v):
    marked = search['marked']
    return mlp.contains(marked, key_v) and mlp.get(marked, key_v) is True

def path_to_bfs(search, key_v):
    if not has_path_to_bfs(search, key_v):
        return None
    path = s.new_stack()
    edge_to = search['edge_to']
    v = key_v
    
    while mlp.contains(edge_to, v) and mlp.get(edge_to, v) is not None:
        s.push(path, v)
        v = mlp.get(edge_to, v)
    s.push(path, v) 
    return path