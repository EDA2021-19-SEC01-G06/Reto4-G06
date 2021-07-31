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


import math
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Sorting import mergesort as sa
from haversineLib.haversine import haversine
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
        "connectionsGr"     :   gr.newGraph("ADJ_LIST", True, 3700, compareLandingsId),
        "landingsById"      :   mp.newMap(loadfactor=2),
        "landingsByName"    :   mp.newMap(loadfactor=2),
        "countries"         :   mp.newMap(loadfactor=2),
    }

    return analyzer


# Funciones para agregar informacion al catalogo

def addLanding(analyzer: dict, landing: dict):
    """
    Agrega un landing point y su información al mapa de landing points por id y
    por nombre del analizador. Se agrega como llave el landing_point_id y como valor
    el diccionario con toda la información del landing point. Crea la estructura
    para almacenar la lista de vertices que corresponden al landing point.
    Adicionalmente crea el país y la estructura de datos vacía.

    Nota: la información completa del landing solo queda almacenada en el mapa de
    landings por Id. En las otras estructuras se almacena solo el id como str.

    Args
    ----
    analyzer: dict[str, Any] -- Analizador
    landing: dict[str, any] -- Diccionario con toda la información del landing a agregar
    """
    # Crea la lista para almacenar los vertices correspondientes al landing
    landing["vertices"] = lt.newList("ARRAY_LIST")
    # Añade el landing al mapa de landings por Id
    mp.put(analyzer["landingsById"], landing["landing_point_id"], landing)
    # Añade el landing al mapa de landings por nombre
    mp.put(analyzer["landingsByName"], landing["name"].strip().lower(), landing["landing_point_id"])
    # Obtiene el nombre del país
    countryName = landing["name"].split(", ")[-1]
    # Crea el país del Landing si no existe
    createCountry(analyzer, countryName)
    # Añade el landing al país
    addLandToCountry(analyzer, landing["landing_point_id"], countryName)


def createCountry(analyzer: dict, countryName: str):
    """
    Crea el país en el mapa de paises si no existe. La llave es el nombre del país y el valor
    es un diccionario que contiene una lista, en la que se almacenarán los landings
    correspondientes al país.

    Args
    -----
    analyzer: dict[str, Any] -- analizador
    countryName: str -- Nombre del país a agregar
    """
    countryName = countryName.strip().lower()
    country = getMapValue(analyzer["countries"], countryName)
    if country is None:
        countryNode = {"landingsById": lt.newList("ARRAY_LIST")}
        mp.put(analyzer["countries"], countryName, countryNode)


def addLandToCountry(analyzer: dict, landingId: str, countryName: str):
    """
    Añade un landing point a la lista de landings de un país

    Args
    ----
    analyzer: dict -- analizadot
    landingId: str -- identificador (numérico) del landing point
    countryName: str -- nombre del país
    """
    countryName = countryName.strip().lower()
    countryLanList = getMapValue(analyzer["countries"], countryName)["landingsById"]
    lt.addLast(countryLanList, landingId)


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
    countryName: str = country["CountryName"].strip().lower()
    countryNode: dict = getMapValue(analyzer["countries"], countryName)
    # Si el país se agregó previamente
    if countryNode is not None:
        # Añade la información del país al diccionario ya existente
        countryNode.update(country)
    else:
        # Crea la lista para los landings del país
        country["landingsById"] = lt.newList("ARRAY_LIST")
        # Añade el país al mapa de paises
        countryNode = country
        mp.put(analyzer["countries"], countryName, countryNode)


    # Crea y conecta la capital al los landing points
    connectCapital(analyzer, countryNode)


def connectCapital(analyzer: dict, country: dict):
    """
    Crea un landing point en la capital del país y conecta la capital
    con todos los landing points del país. Si el país no tiene landings
    connecta la capital con el landing point mas cercano.

    Args
    ----
    analyzer: dict -- Analizador
    country: dict[str, Any] -- diccionario con la información del país. Debe
        contener la llave landings

    Returns: bool
    -------
    True si se pudo conectar, false si no.
    """
    # Si el país no tiene capital, no hace nada
    if country["CapitalName"] == "":
        return False
    
    # Crea la información del landing point
    capitalNameId = country["CapitalName"].strip().lower().replace(" ", "")
    landingNode = {
        "landing_point_id"  : capitalNameId,
        "name"              : country["CapitalName"] + ", " + country["CountryName"],
        "latitude"          : country["CapitalLatitude"],
        "longitude"         : country["CapitalLongitude"],
        "vertices"          : lt.newList("ARRAY_LIST")
    }

    # Añade el landing al mapa de landings
    addLanding(analyzer, landingNode)

    # Crea el vertice en el grafo de conecciones
    cableName = country["CountryName"] + "_terrestre"
    vertexA = addConVertex(analyzer, capitalNameId, cableName)

    # Crea la conección a todas los landings del país
    #Si no hay landings en el país
    if lt.isEmpty(country["landingsById"]):
        #Busca el landing mas cercano
        nearestId, cableLength = fNearestLand(landingNode)[0]
        # Crea el vertice del landing mas cercano
        vertexB = addConVertex(analyzer, nearestId, cableName)
    #Si sí hay landings
    else:
        #Ciclo por los landings del país
        for orgDest in lt.iterator(country["landingsById"]):
            # Calcula la distance
            orgDestNode = getMapValue(analyzer["landingsById"], orgDest)
            cableLength = calcLanDistance(orgDestNode, landingNode)
            # Crea el vertice de orgDest
            vertexB = addConVertex(analyzer, orgDest, cableName)

    # Crea las conecciones
    gr.addEdge(analyzer["connectionsGr"], vertexA, vertexB, cableLength)
    gr.addEdge(analyzer["connectionsGr"], vertexB, vertexA, cableLength)


def addConnection(analyzer: dict, connection: dict):
    """
    Agrega una conección al grafo de conecciones. Los vertices son los landings
    de la conección y el costo es de la forma "<origin_id>-<destination_id>". Adicionalmente, agrega la
    connección y su información al mapa de conecciones donde la llave es de la forma
    "<origin_id>-<destination_id>" y el valor es toda la información de esta.

    Args
    ----
    analyzer: dict[str, Any] -- Analizador
    connection: dict[str, Any] -- Diccionario con toda la información de la conección a agregar
    """
    try:
        cableLength = float(connection["cable_length"].strip(" km").replace(",", ""))
    except ValueError:
        # Si no se logra obtener la distancia entre 2 landing points, se calcula
        landing1 = getMapValue(analyzer["landingsById"], connection["origin"])
        landing2 = getMapValue(analyzer["landingsById"], connection["destination"])
        cableLength = calcLanDistance(landing1, landing2)
    # Añade el vertice de origen
    vertexA = addConVertex(analyzer, connection["origin"], connection["cable_id"])
    # Añade el vertice de destino
    vertexB = addConVertex(analyzer, connection["destination"], connection["cable_id"])
    # Añade el arco
    gr.addEdge(analyzer["connectionsGr"], vertexA, vertexB, cableLength)


def addConVertex(analyzer: dict, landing: str, cable: str):
    """
    Agrega un vertice al grafo de conecciones de la forma "<landing>-<cable>".
    Adicionalmente, agrega el vertice a la lista de vertices del landing point.

    Args
    ----
    analyzer: dict -- Analizador
    landing: str -- identificador (numérico) del landing point
    cable: str -- identificador del cable
    """
    vertexName = landing + "-" + cable
    gr.insertVertex(analyzer["connectionsGr"], vertexName)
    landingVerLst = getMapValue(analyzer["landingsById"], landing)["vertices"]
    lt.addLast(landingVerLst, vertexName)

    return vertexName


def groupLandings(analyzer: dict):
    """
    Itera por todos los landings y conecta los vertices que comparten un mismo landing

    Args
    ----
    analyzer: dict -- analizador
    """
    landingsLst = mp.valueSet(analyzer["landingsById"])

    for landing in lt.iterator(landingsLst):
        verticesLst = landing["vertices"]
        # Connecta del primero al último
        for i in range(1, lt.size(verticesLst)):
            vertexA = lt.getElement(verticesLst, i)
            vertexB = lt.getElement(verticesLst, i + 1)
            gr.addEdge(analyzer["connectionsGr"], vertexA, vertexB, 0)
        # Conecta el último con el primero
        vertexA = lt.getElement(verticesLst, lt.size(verticesLst))
        vertexB = lt.getElement(verticesLst, 1)
        gr.addEdge(analyzer["connectionsGr"], vertexA, vertexB, 0)


# Funciones para creacion de datos

# Funciones de consulta

def fNearestLand(analyzer: dict, landing1: dict) -> str:
    """
    Busca el landing point mas cercano a aquel pasado por parámetro, utilizando
    la formula de distancia de Haversine.

    Args
    ----
    analyzer: dict -- analizador
    landing1: dict -- diccionario con información del landing

    Returns
    -------
    str -- identificador del landing más cercano
    """
    landingsLst = mp.valueSet(analyzer["landingsById"])
    crrntMinDistance = math.inf
    # Ciclo por todos los landings
    for landing2 in lt.iterator(landingsLst):
        # Evita comparar el landing1 con si mismo
        if not landing2["landing_point_id"] == landing1["landing_point_id"]:
            distance = calcLanDistance(landing1, landing2)
            if distance < crrntMinDistance:
                crrntMinDistance = distance
                crrntClosest = landing2["landing_point_id"]

    return crrntClosest, crrntMinDistance
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# ========================
# Funciones de comparación
# ========================

def compareLandingsId(landingId1, keyValLanId):
    """
    Compara el id de dos estaciones. Se utiliza para
    la implementación del grafo de conecciones.
    """
    landingId2 = keyValLanId['key']
    if (landingId1 == landingId2):
        return 0
    elif (landingId1 > landingId2):
        return 1
    else:
        return -1

# ==========================
#       Otras funciones
# ==========================

def getMapValue(map, key):
    """
    Devuelve el valor correspondiente a la llave pasada por parámetro
    o None si no encuentra la llave en el mapa
    """
    entry = mp.get(map, key)
    if entry == None:
        return None
    value = me.getValue(entry)
    return value


def calcLanDistance(landingA: dict, landingB: dict) -> float:
    """
    Calcula la distancia entre dos landing points utilizando la formula de
    distancia de Haversine.

    Args
    ----
    landingA: dict -- diccionario con la información del landing point 1
    landingB: dict -- diccionario con la información del landing point 2

    Returns
    -------
    float -- distancia en kilometros
    """
    latLon1 = (float(landingA["latitude"]), float(landingA["longitude"]))
    latLon2 = (float(landingB["latitude"]), float(landingB["longitude"]))
    distaceKm = haversine(latLon1, latLon2)

    return distaceKm