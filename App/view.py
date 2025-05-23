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


import sys
import threading

from App import logic

# Nombre del archivo CSV en /Data
SERVICE_FILE = 'bus_routes_14000.csv'


def print_menu():
    print("\n" + "*" * 50)
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de Singapur")
    print("3- Calcular componentes conectados")
    print("4- Establecer estación base")
    print("5- Hay camino entre estación base y estación")
    print("6- Ruta de costo mínimo desde la estación base y estación")
    print("7- Estación que sirve a más rutas")
    print("8- Existe un camino de búsqueda entre la estación base y estación destino")
    print("9- Ruta de búsqueda entre la estación base y estación destino")
    print("0- Salir")
    print("*" * 50)


def option_one():
    print("\nInicializando analizador...")
    analyzer = logic.init()
    print("Analizador inicializado.")
    return analyzer


def option_two(analyzer):
    print("\nCargando información de transporte de Singapur...")
    analyzer = logic.load_services(analyzer, SERVICE_FILE)
    v = logic.total_stops(analyzer)
    e = logic.total_connections(analyzer)
    print(f"Número de vértices (paradas): {v}")
    print(f"Número de arcos   (conexiones): {e}")
    return analyzer


def option_three(analyzer):
    print("\nCalculando componentes conectados...")
    n_comp = logic.connected_components(analyzer)
    print(f"Número de componentes conectados: {n_comp}")


def option_four(analyzer):
    station = input("Ingrese código de la estación base (formato STOPID-SERVICE): ")
    ok = logic.set_station(analyzer, station)
    if ok:
        print(f"Estación base establecida en '{station}'.")
    else:
        print(f"No existe la estación '{station}' en el grafo.")


def option_five(analyzer):
    dest = input("Ingrese código de la estación destino: ")
    has = logic.has_path_to(analyzer, dest)
    print(f"¿Hay camino de '{analyzer.get('base_station')}' a '{dest}'? {'Sí' if has else 'No'}")


def option_six(analyzer):
    dest = input("Ingrese código de la estación destino: ")
    path = logic.path_to(analyzer, dest)
    if path:
        # Supongo que path es una pila; extraigo y muestro de base a destino
        ruta = []
        while not path.is_empty():
            ruta.append(path.pop())
        print("Ruta de costo mínimo:", " → ".join(reversed(ruta)))
        costo = logic.dist_to(analyzer, dest)
        print(f"Costo total: {costo}")
    else:
        print("No existe ruta.")


def option_seven(analyzer):
    station, count = logic.station_with_most_routes(analyzer)
    print(f"Estación que sirve a más rutas: {station} ({count} rutas)")


def option_eight(analyzer):
    dest = input("Ingrese código de la estación destino: ")
    has = logic.has_path_bfs(analyzer, dest)
    print(f"¿Existe un camino BFS de '{analyzer.get('base_station')}' a '{dest}'? {'Sí' if has else 'No'}")


def option_nine(analyzer):
    dest = input("Ingrese código de la estación destino: ")
    path = logic.path_bfs(analyzer, dest)
    if path:
        ruta = []
        while not path.is_empty():
            ruta.append(path.pop())
        print("Ruta BFS:", " → ".join(reversed(ruta)))
    else:
        print("No existe ruta.")


def main():
    analyzer = None
    while True:
        print_menu()
        choice = input("> ").strip()

        if choice == '1':
            analyzer = option_one()

        elif choice == '2':
            if analyzer is None:
                print("Primero inicialice el analizador (opción 1).")
            else:
                analyzer = option_two(analyzer)

        elif choice == '3':
            if analyzer is None:
                print("Primero inicialice el analizador (opción 1).")
            else:
                option_three(analyzer)

        elif choice == '4':
            if analyzer is None:
                print("Primero inicialice el analizador (opción 1).")
            else:
                option_four(analyzer)

        elif choice == '5':
            if analyzer is None or analyzer.get('dijkstra_search') is None:
                print("Primero establezca la estación base (opción 4).")
            else:
                option_five(analyzer)

        elif choice == '6':
            if analyzer is None or analyzer.get('dijkstra_search') is None:
                print("Primero establezca la estación base (opción 4).")
            else:
                option_six(analyzer)

        elif choice == '7':
            if analyzer is None:
                print("Primero inicialice el analizador (opción 1).")
            else:
                option_seven(analyzer)

        elif choice == '8':
            if analyzer is None:
                print("Primero inicialice el analizador (opción 1).")
            else:
                option_eight(analyzer)

        elif choice == '9':
            if analyzer is None:
                print("Primero inicialice el analizador (opción 1).")
            else:
                option_nine(analyzer)

        elif choice == '0':
            print("Saliendo...")
            sys.exit(0)

        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    # Aumentar stack y recursión para DFS si hace falta
    threading.stack_size(67108864)
    sys.setrecursionlimit(2 ** 20)
    main()