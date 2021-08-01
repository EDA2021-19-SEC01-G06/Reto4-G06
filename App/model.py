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

import DISClib.Algorithms.Graphs.scc as scc
from DISClib.Algorithms.Graphs import dijsktra as djk
import math
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr, numEdges, vertices
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
        "highestLandingId"  :   -1
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
    # Le da formato al nombre del Landing
    landing["name"] = formatLanName(landing["name"])
    # Añade el landing al mapa de landings por Id
    mp.put(analyzer["landingsById"], landing["landing_point_id"], landing)
    # Añade el landing al mapa de landings por nombre
    mp.put(analyzer["landingsByName"], landing["name"].strip().lower(), landing["landing_point_id"])
    # Actualiza el valor de highestLandingId
    if int(landing["landing_point_id"]) > analyzer["highestLandingId"]:
        analyzer["highestLandingId"] = int(landing["landing_point_id"])
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

    # Obtiene el landing en la capital
    landingNode = createCapitalLan(analyzer, country)


    # Crea la conección a todas los landings del país
    # Si no hay landings en el país
    if lt.isEmpty(country["landingsById"]):
        # Crea el vertice A en el grafo de conecciones
        cableName = country["CountryName"] + "_ter1"
        vertexA = addConVertex(analyzer, landingNode["landing_point_id"], cableName)
        #Busca el landing mas cercano
        nearestId, cableLength = fNearestLand(analyzer, landingNode)
        # Crea el vertice B del landing mas cercano
        vertexB = addConVertex(analyzer, nearestId, cableName)
        # Crea las conecciones
        gr.addEdge(analyzer["connectionsGr"], vertexA, vertexB, cableLength)
        gr.addEdge(analyzer["connectionsGr"], vertexB, vertexA, cableLength)
    #Si sí hay landings
    else:
        #Ciclo por los landings del país
        i = 1
        for orgDest in lt.iterator(country["landingsById"]):
            # Crea el vertice A en el grafo de conecciones
            cableName = country["CountryName"] + "_ter" + str(i)
            i += 1
            vertexA = addConVertex(analyzer, landingNode["landing_point_id"], cableName)
            # Calcula la distance
            orgDestNode = getMapValue(analyzer["landingsById"], orgDest)
            cableLength = calcLanDistance(orgDestNode, landingNode)
            # Crea el vertice B de orgDest
            vertexB = addConVertex(analyzer, orgDest, cableName)
            # Crea las conecciones
            gr.addEdge(analyzer["connectionsGr"], vertexA, vertexB, cableLength)
            gr.addEdge(analyzer["connectionsGr"], vertexB, vertexA, cableLength)

    return True

def createCapitalLan(analyzer: dict, country: dict):
    """
    Crea añade y retorna un landingNode con la información de la capital de un país.
    Si la capital ya existe, retorna la información de la capital ya existente.

    Args
    ----
    analyzer: dict -- analizador
    country: dict -- diccionario con la información del país.

    Returns
    --------
    dict -- diccionario con la información del landing en la capital
    """
    # Crea el nombre del landing point
    lanName = (country["CapitalName"] + ", " + country["CountryName"]).strip().lower()
    # Revisa si ya existe un landing en la capital
    existingCapLanId = getMapValue(analyzer["landingsByName"], lanName)
    if existingCapLanId is not None:
        # Obtiene el nodo de landing existente
        landingNode = getMapValue(analyzer["landingsById"], existingCapLanId)

        return landingNode
    else:
        # Si no existe un landing en la capital
        # Crea la información del landing point
        landingNode = newLandingNode(
            analyzer,
            country["CapitalName"] + ", " + country["CountryName"],
            country["CapitalLatitude"],
            country["CapitalLongitude"]
        )
        # Añade el landing al mapa de landings
        addLanding(analyzer, landingNode)

        return landingNode


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
    # Si ya existe un vertice con esas condiciones
    if gr.containsVertex(analyzer["connectionsGr"], vertexName):
        return vertexName

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

def newLandingNode(analyzer: dict, name: str, lat: str, lon: str, lanPId: str = None, vertices = None):
    """
    Crea el diccionario que contiene la información necesaria para un Landing.
    El diccionario contiene llaves landing_point_id, name, latitude, longitude,
    vertices.

    Args
    ----
    analyzer: dict -- analizador
    name: str -- Nombre del landing point de la forma "<city>, <country>"
    lat: str -- Latitud del landing point
    lon: str -- Longitud del landing point
    lanPId: str, optional -- id (numerico) del landing point. Si no se pasa
    se asigna automáticamente un id.
    vertices: optional -- TAD lista con vertices que corresponden a ese landing point.
    Si no se pasa por parámetro, se inicializa una lista vacia.

    Returns
    -------
    dict -- Diccionario con la información del landing
    """
    if lanPId is None:
        lanPId = str(analyzer["highestLandingId"] + 1)

    if vertices is None:
        vertices = lt.newList("ARRAY_LIST")
    
    landingNode = {
        "landing_point_id"  : lanPId,
        "name"              : name,
        "latitude"          : lat,
        "longitude"         : lon,
        "vertices"          : vertices
    }

    return landingNode


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
    # Obtiene el Id a partir del vertexName
    landPId = vertexName.split("-")[0]
    # Obtiene el landing a partir del Id
    landing = getMapValue(analyzer["landingsById"], landPId)

    if landing is None:
        raise Exception("Landing not found")
    
    return landing


def findClusters(analyzer: dict, landing1Name: str, landing2Name: str):
    """
    Encuentra los componentes fuertemente conectados del grafo conecciones
    y revisa si dos landing points están fuertemente conectados.

    Args
    ----
    analyzer: dict -- analizador
    landing1Name: str -- nombre del landing point 1
    landing2Name: str -- nombre del landing point 2

    Returns
    -------
    dict -- diccionario que contiene las siguientes llaves:
        "vertexA": vertice correspondiente al landing 1 pasado por parámetro
        "vertexB": vertice correspondiente al landing 2 pasado por parámetro
        "stronglyC": True si los landings están fuertemente conectados o False
            si no lo están
        "components": (int) número de componentes fuertemente conectados
    """
    # Encuentra los componentes fuertemente conectados
    componentsscc = (scc.KosarajuSCC(analyzer['connectionsGr']))
    # Obtiene el total de componentes conectados
    totalscc = scc.connectedComponents(componentsscc)
    # Obtiene el id de los landings
    landingid1 = getMapValue(analyzer['landingsByName'], landing1Name)
    landingid2 = getMapValue(analyzer['landingsByName'], landing2Name)
    # Obtiene la información completa de los landings
    landingNode1 = getMapValue(analyzer["landingsById"], landingid1)
    landingNode2 = getMapValue(analyzer["landingsById"], landingid2)
    # Obtiene un vertice correspondiente a cada landing
    vertex1 = lt.getElement(landingNode1["vertices"], 1)
    vertex2 = lt.getElement(landingNode2["vertices"], 1)
    # Revisa si los vertices están fuertemente conectados.
    stronglyC = scc.stronglyConnected(componentsscc, vertex1, vertex2)
    # Crea la estructura a retornar
    returnDict = {
        "vertexA"       :   vertex1,
        "vertexB"       :   vertex2,
        "stronglyC"     :   stronglyC,
        "components"    :   totalscc
    }
    
    return returnDict


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
    # Obtiene la información de los paises
    countryNode1 = getMapValue(analyzer["countries"], countryName1)
    countryNode2 = getMapValue(analyzer["countries"], countryName2)
    # Obtiene el vertice correspondiente la capital 2
    lanName1 = (countryNode1["CapitalName"] + ", " +  countryNode1["CountryName"]).strip().lower()
    lanId1 = getMapValue(analyzer["landingsByName"], lanName1)
    lanNode1 = getMapValue(analyzer["landingsById"], lanId1)
    vertex1 = lt.getElement(lanNode1["vertices"], 1)
    # Obtiene el vertice correspondiente a la capital 2
    lanName2 = (countryNode2["CapitalName"] + ", " +  countryNode2["CountryName"]).strip().lower()
    lanId2 = getMapValue(analyzer["landingsByName"], lanName2)
    lanNode2 = getMapValue(analyzer["landingsById"], lanId2)
    vertex2 = lt.getElement(lanNode2["vertices"], 1)
    # Encuentra los caminos mínimos del countryNode1 a todos los demás
    paths = djk.Dijkstra(analyzer["connectionsGr"], vertex1)
    # Verifica si existe una ruta entre los dos puntos
    if not djk.hasPathTo(paths, vertex2):
        return {"status":   0}
    # Encuentra la ruta de costo mínimo entre el origen y el destino
    path = djk.pathTo(paths, vertex2)
    # Crea la estructura de retorno
    returnDict = {
        "status"    :   1,
        "path"      :   path,
        "origin"    :   vertex1,
        "dest"      :   vertex2
    }

    return returnDict


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
    distaceKm = round(haversine(latLon1, latLon2), 2)

    return distaceKm


def formatLanName(lanName: str) -> str:
    """
    Da formato al nombre del landing de la forma "<city>, <country>"
    para estandarizar el nombre de los landings.
    *Note que algunos landings tienen un nombre de la forma "<city>, <state>,
    <country>" originalmente. En esos caso se elimina <state>

    Args
    ----
    lanName: str -- nombre original del landing

    Returns
    -------
    str -- nombre del landing formateado
    """
    lanNDict = lanName.split(",")
    lanName = lanNDict[0].strip() + ", " + lanNDict[-1].strip()

    return lanName