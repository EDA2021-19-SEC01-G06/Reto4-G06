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
 """

import config as cf
import model
import csv
from mtTraceLib.mtTrace import mtTrace
import time
import tracemalloc

mtt = mtTrace()

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del analizador

def initAnalyzer():
    """
    Inicializa el analizador
    """
    analyzer = model.initAnalyzer()
    
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer: dict):
    """
    Carga la información de los archivos

    Args
    ----
    analyzer: dict [str, Any] -- Analizador
    """
    #Start memory and time trace
    mtt.start()
    
    firstLanding    =   loadLandings(analyzer)
    loadConnections(analyzer)
    lastCountry     =   loadCountries(analyzer)
    # Conecta los vertices que tienen un landing común
    model.groupLandings(analyzer)

    
    returnDict = {
        "firstLanding": firstLanding,
        "lastCountry": lastCountry
    }

    #Stop memory and time trace
    mtt.stop()
    
    return returnDict

def loadCountries(analyzer: dict) -> dict:
    """
    Carga la información de los paises desde los archivos.

    Args
    ----
    analyzer: dict[str, Any] -- Analizador
    """
    file_path = cf.data_dir + "countries.csv"
    input_file = csv.DictReader(open(file_path, encoding="utf-8"),
                                delimiter=",")
    for country in input_file:
        model.addCountry(analyzer, country)
        lastCountry = country

    return country


def loadLandings(analyzer: dict) -> dict:
    """
    Carga la información de los landing points desde los archivos.

    Args
    ----
    analyzer: dict[str, Any] -- Analizador

    Returns: dict[str, Any]
    -------
    El diccionario con la información del primer landing cargado
    """
    file_path = cf.data_dir + "landing_points.csv"
    input_file = csv.DictReader(open(file_path, encoding="utf-8"),
                                delimiter=",")
    #First landing element
    firstLanding = next(input_file)
    model.addLanding(analyzer, firstLanding)
    #Rest of the landing elements
    for landing in input_file:
        model.addLanding(analyzer, landing)

    return firstLanding

def loadConnections(analyzer: dict):
    """
    Carga la información de las conecciones desde los archivos.

    Args
    ----
    analyzer: dict[str, Any] -- Analizador
    """
    file_path = cf.data_dir + "connections.csv"
    input_file = csv.DictReader(open(file_path, encoding="utf-8-sig"),
                                delimiter=",")
    for connection in input_file:
        model.addConnection(analyzer, connection)


def getLanFromVer(analyzer: dict, vertexName: str):
    """
    Obtiene el landing point correspondiente a un vertice del grafo connections.

    Args:
    -----
    analyzer: dict -- analizador
    vertexName: str -- nombre del vertice de la forma "<landingId>-<cableId>"

    Returns
    -------
    dict -- diccionario con la información del landing point
    """
    return model.getLanFromVer(analyzer, vertexName)


def findClusters(analyzer, landing1Name, landing2Name):
    """
    TODO documentación
    """
    mtt.start()
    ans = model.findClusters(analyzer, landing1Name, landing2Name)
    mtt.stop()
    return ans


def minimumRoute(analyzer: dict, countryName1: str, countryName2: str):
    """
    Encuentra la ruta mínima entre las capitales de dos paises.

    Args
    ----
    analyzer: dict -- analizador
    countryName1: str -- nombre del país 1
    countryName2: str -- nombre del país 2

    Returns
    -------
    dict -- diccionario con llaves:
        status: (int) 0 si NO se encontró la ruta, 1 si se encontró
        path:   información de la ruta
        origin: vertice de origen
        dest:   vertice de destino
    """

    mtt.start()
    ans= model.minimumRoute(analyzer, countryName1, countryName2)
    mtt.stop()

    return ans



def minimumSpanNet(analyzer: dict):
    """
    Encuentra la red de expansión mínima del grafo conecciones

    Args
    ----
    analyzer: dict -- analizador

    Returns
    -------
    TODO
    """
    mtt.start()
    ans= model.minimumSpanNet(analyzer)
    mtt.stop()

    return ans

    


def longestMSTbranch(edgesTo, originVer: str):
    """
    Encuentra la rama mas larga del MST.

    Args
    ----
    analyzer: dict -- analizador
    edgesTo -- TAD map edgesTo del MST devuelto por el algorimo PRIM
    originVer: str -- Vertice de origen con el que se calculó el MST

    Returns
    -------
    int -- longitud de la rama mas larga
    """
    mtt.start()
    ans = model.longestMSTbranch(edgesTo, originVer)
    mtt.stop()
    return ans

    
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
