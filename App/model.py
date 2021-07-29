"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as sa
from DISClib.ADT.graph import gr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def initAnalyzer() -> dict:
    """
    Inicializa el analizador

    Returns: dict[str, Any]
    -------
    El analizador inicializado
    """
    analyzer = {
        "conections"    :   gr.newGraph("ADJ_LIST", False, 100), #TODO determinar tamaño
        "landings"      :   mp.newMap(loadfactor=2),
        "countries"     :   mp.newMap(loadfactor=2)
    }

    return analyzer


# Funciones para agregar informacion al catalogo

def addCountry(analyzer: dict, country: dict):
    """
    Agrega un país y su información al mapa de paises del analizador.
    Se agrega como llave el nombre del país (en minúsculas) y como valor
    el diccionario con toda la información del país.

    Args
    ----
    analyzer: dict[str, Any] -- Analizador
    country: dict[str, Any] -- Diccionario con toda la información del país a agregar
    """
    mp.put(analyzer["countries"], country["Country Name"], country)


def addLanding(analyzer: dict, landing: dict):
    """
    Agrega in landing point y su información al mapa de landing points
    del analizador. Se agrega como llave el landing_point_id y como valor
    el diccionario con toda la información del landing point.
    Adicionalmente, agrega el landing point como vertice del grafo de conecciones
    del analizador. La llave del vertice corresponde al landing_point_id del landing

    Args
    ----
    analyzer: dict[str, Any] -- Analizador
    landing: dict[str, any] -- Diccionario con toda la información del landing a agregar
    """
    mp.put(analyzer["landings"], landing["landing_point_id"], landing)
    gr.insertVertex(analyzer["conections"], landing["landing_point_id"])

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
