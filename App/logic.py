"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

# ___________________________________________________
#  Importaciones
# ___________________________________________________

import csv
import time
import os

from DataStructures.Graph import edge as ed
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import diagraph as G
from DataStructures.Graph import bfs as gbfs
from DataStructures.Graph import dfs as gdfs
from DataStructures.Graph import prim as prim
from DataStructures.Graph import dijkstra as dk

from DataStructures.List import single_linked_list as lt

from DataStructures.Map import map_entry as me
from DataStructures.Map import map_funtions as mf
from DataStructures.Map import map_linear_probing as m

from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as s

# ---------------------------------------------------
#  Inicialización del analizador
# ---------------------------------------------------

def init():
    """Crea y retorna el analizador vacío"""
    return new_analyzer()


def new_analyzer():
    """Inicializa estructuras de datos principales"""
    analyzer = {
        'stops': None,
        'connections': None,
        'dijkstra_search': None,
        'bfs_search': None,
        'base_station': None
    }
    # Tabla hash para rutas por estación
    analyzer['stops'] = m.new_map(num_elements=14000, load_factor=0.7, prime=109345121)
    # Grafo dirigido para conexiones de paradas
    analyzer['connections'] = G.new_graph(14000)
    return analyzer

# ---------------------------------------------------
#  Carga de datos
# ---------------------------------------------------

def load_services(analyzer, servicesfile):
    """Carga CSV y agrega conexiones de paradas consecutivas."""
    base_dir = os.path.dirname(__file__)
    project_root = os.path.normpath(os.path.join(base_dir, '..'))
    data_dir = os.path.join(project_root, 'Data')
    full_path = os.path.join(data_dir, servicesfile)

    with open(full_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        last = None
        for service in reader:
            if last and last['ServiceNo']==service['ServiceNo'] \
                   and last['Direction']==service['Direction'] \
                   and last['BusStopCode']!=service['BusStopCode']:
                add_stop_connection(analyzer, last, service)
            last = service
    return analyzer

# ---------------------------------------------------
#  Establecer estación base
# ---------------------------------------------------

def set_station(analyzer, station):
    """Configura estación base y ejecuta Dijkstra y BFS."""
    try:
        station = str(station)
        # validación de existencia
        if not G.contains_vertex(analyzer['connections'], station):
            return False
        # Dijkstra para rutas de costo mínimo
        analyzer['dijkstra_search'] = dk.dijkstra(analyzer['connections'], station)
        # BFS para rutas de búsqueda
        analyzer['bfs_search'] = gbfs.bfs(analyzer['connections'], station)
        analyzer['base_station'] = station
        return True
    except Exception as e:
        return e

# ---------------------------------------------------
#  Consultas básicas
# ---------------------------------------------------

def total_stops(analyzer):
    """Número de vértices (paraderos)."""
    return G.order(analyzer['connections'])


def total_connections(analyzer):
    """Número de arcos (conexiones)."""
    return G.size(analyzer['connections'])

# ---------------------------------------------------
#  Componentes conectados
# ---------------------------------------------------

def connected_components(analyzer):
    """Cuenta cuántos componentes en el grafo (trata dirigido como no dirigido)."""
    visited = mf.new_map(G.order(analyzer['connections']))
    count = 0
    for u in mf.key_set(analyzer['connections']['vertices']):
        if not mf.contains_key(visited, u):
            count += 1
            _dfs_mark(analyzer['connections'], u, visited)
    return count


def _dfs_mark(graph, u, visited):
    mf.put(visited, u, True)
    # visitar vecinos salientes
    for v in G.adjacents(graph, u).elements:
        if not mf.contains_key(visited, v):
            _dfs_mark(graph, v, visited)
    # visitar vecinos entrantes
    for w in mf.key_set(graph['vertices']):
        if G.get_edge(graph, w, u) is not None and not mf.contains_key(visited, w):
            _dfs_mark(graph, w, visited)

# ---------------------------------------------------
#  Rutas y caminos
# ---------------------------------------------------

def has_path_to(analyzer, dest):
    """¿Existe un camino de mínima distancia a dest?"""
    return dk.has_path_to(dest, analyzer['dijkstra_search'])


def path_to(analyzer, dest):
    """Stack con ruta de mínima distancia a dest."""
    return dk.path_to(dest, analyzer['dijkstra_search'])


def dist_to(analyzer, dest):
    """Costo de mínima distancia a dest."""
    return dk.dist_to(dest, analyzer['dijkstra_search'])


def has_path_bfs(analyzer, dest):
    """¿Existe un camino BFS a dest?"""
    return gbfs.has_path_to_bfs(analyzer['bfs_search'], dest)


def path_bfs(analyzer, dest):
    """Stack con ruta BFS a dest."""
    return gbfs.path_to_bfs(analyzer['bfs_search'], dest)

# ---------------------------------------------------
#  Estación con más rutas
# ---------------------------------------------------

def station_with_most_routes(analyzer):
    """Retorna (estación, número de rutas) con más rutas."""
    max_stop, max_count = None, 0
    for stop in mf.key_set(analyzer['stops']):
        routes = mf.get(analyzer['stops'], stop)
        # si usas list_node, extrae value
        count = len(routes.elements) if hasattr(routes, 'elements') else routes.size
        if count > max_count:
            max_stop, max_count = stop, count
    return max_stop, max_count

# ---------------------------------------------------
#  Helpers de grafo
# ---------------------------------------------------

def add_stop_connection(analyzer, prev_s, curr_s):
    o = format_vertex(prev_s)
    d = format_vertex(curr_s)
    clean_distance(prev_s, curr_s)
    dist = abs(float(curr_s['Distance']) - float(prev_s['Distance']))
    add_stop(analyzer, o)
    add_stop(analyzer, d)
    G.add_edge(analyzer['connections'], o, d, dist)
    add_route_stop(analyzer, curr_s)
    add_route_stop(analyzer, prev_s)
    return analyzer


def add_stop(analyzer, stopid):
    if not G.contains_vertex(analyzer['connections'], stopid):
        G.insert_vertex(analyzer['connections'], stopid, stopid)
    return analyzer


def add_route_stop(analyzer, service):
    code = service['BusStopCode']
    routes = mf.get(analyzer['stops'], code)
    if routes is None:
        lst = lt.new_list()
        lt.add_last(lst, service['ServiceNo'])
        mf.put(analyzer['stops'], code, lst)
    else:
        # rutas en single_linked_list: extraer con .elements o iterador
        lst = routes
        if not lt.is_present(lst, service['ServiceNo']):
            lt.add_last(lst, service['ServiceNo'])
    return analyzer


def clean_distance(s1, s2):
    if s1['Distance']=='': s1['Distance']='0'
    if s2['Distance']=='': s2['Distance']='0'


def format_vertex(service):
    return f"{service['BusStopCode']}-{service['ServiceNo']}"

# ---------------------------------------------------
#  Medición de tiempos
# ---------------------------------------------------

def get_time():      return float(time.perf_counter()*1000)

def delta_time(e, s): return float(e - s)