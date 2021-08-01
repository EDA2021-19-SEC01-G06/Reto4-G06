"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

from os import sep
import config as cf
import sys
import controller
import geoMap
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
import threading
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ==============================
#    Input / Output funciont
# ==============================

def printRow(row: list) -> None:
    """
    Imprime la fila de una tabla. Si el largo de los datos supera el ancho de la columna,
    imprime el dato incompleto con ...
    Args:
        row: Lista de listas. Row debe ser de la forma [<lens>, <data>]
            <lens>: (list) Lista con ancho de las columnas
            <data>: (list) Lista con datos de las columnas
    TODO Manejo de ancho y caracteres asiaticos
    """
    rowFormat = ""
    for i in range(0, len(row[0])):
        colWidth = row[0][i]
        cell = str(row[1][i])
        #Añade la columna al formato
        rowFormat += "{:<" + str(colWidth) + "}"
        #Revisa y corrige si el tamaño de los datos es más grande que la columna
        if len(cell) > colWidth:
            row[1][i] = cell[0:colWidth - 3] + "..."
    
    #Imrpime la fila
    print(rowFormat.format(*row[1]))


def eoc() -> None:
    """
    Le permite al usuario salir o continuar con la ejecución del programa.
    """
    if input("ENTER para continuar o 0 para salir: ") == "0":
        sys.exit(0)


def printMenu():
    """
    Imprime las opciones del menú
    """
    print("Bienvenido")
    print("1- Cantidad de Clusters")
    print("2- Encontrar ruta mínima")
    print("3- Encontrar red de expanción mínima")
    print("0- Salir")
    #TODO Bono


def userInput(prompt: str, Intype = str, validateFunc = None, validateMap = None,
    notFPromt: str = "Entrada invalida, intente nuevamente"):
    """
    Valida si el input que dio el usuario es valido. Utiliza validateFunc
    o validateMap para lo anterior. Si el input no es valido, itera hasta
    que el usuario ingrese un input valido.

    Args
    ----
    promt: str -- Mensaje para el input
    Intype: type -- tipo al que se debe convertir el input para validarlo, por ejemplo int.
        El tipo debe ser una clase cuya función de inicialización reciba un str y lo convierta
        al tipo deseado.
    validateFunc: function -- función que recibe un solo argumento (el input del usuario, convertido al tipo
        pasado por parámetro). La función retorna True si la entrada es valida o False si no lo es.
        Si no se espcifica, se utiliza validateMap para validar la entrada-
    validateMap -- mapa en el que se revisa si existe una entrada cuya llave corresponda a el input
        del usuario convertido al tipo especificado por parámetro. Si existe la entrada, se considera
        que el input del usuario es valido, de lo contrario, se considera que el input del usuario
        es invalido.
    notFPromt: str -- Texto a imprimir si la entrada es inválida
    
    Returns
    -------
    El input del usuario convertido al tipo especificado por parámetro
    """
    # Si no hay manera de validar
    if validateFunc is None and validateMap is None:
        raise Exception("No se especificó validateMap ni validateFunc.")
    # Si se especifico validar con función
    elif validateFunc is not None:
        first = True
        inputs = None
        while first or (validateFunc(inputs) == False):
            if not first:
                print(notFPromt)
            first = False
            inputs = Intype(input(prompt).strip().lower())
        
        return inputs
    # Si se especificó validar con map
    elif validateMap is not None:
        first = True
        inputs = None
        while first or (getMapValue(validateMap, inputs) is None):
            if not first:
                print(notFPromt)
            first = False
            inputs = Intype(input(prompt).strip().lower())
        
        return inputs
    


# =======================
#   Program functions
# =======================

def init():
    print("A continuación se cargará la información de los archivos")
    eoc()
    print("Cargando...")
    #Load data
    analyzer = controller.initAnalyzer()
    loadInfo = controller.loadData(analyzer)
    firstLanding = loadInfo["firstLanding"]
    lastCountry = loadInfo["lastCountry"]
    #Print loading result
    print("\nLanding points cargados:", mp.size(analyzer["landingsById"]))
    print("Conecciones cargadas:", gr.numEdges(analyzer["connectionsGr"]))
    print("Paises cargados:", mp.size(analyzer["countries"]))
    print()
    controller.mtt.printTrace()
    print()
    #Info del primer landing cargado
    print("\n**Primer landing point cargado**")
    printRow([
        [10, 30, 10, 10],
        ["id", "name", "lat", "long"]
    ])
    printRow([
        [10, 30, 10, 10],
        [firstLanding["landing_point_id"], firstLanding["name"], firstLanding["latitude"],
        firstLanding["longitude"]]
    ])
    #Info del último país cargado
    print("\n**Último país cargado**")
    printRow([
        [20, 20, 20],
        ["Name", "Population", "Internet users"]
    ])
    printRow([
        [20, 20, 20],
        [lastCountry["CountryName"], lastCountry["Population"], lastCountry["Internet users"]]
    ])
    print()
    eoc()
    #Ejecuta el menú principal
    mainMenu(analyzer)


def mainMenu(analyzer):
    """
    Ciclo. Menú principal.
    """
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            #REQ 1
            findClusters(analyzer)
        elif int(inputs[0]) == 2:
            #REQ 2
            minimunRoute(analyzer)
        elif int(inputs[0]) == 3:
            #REQ3
            minimumSpanNet(analyzer)
        else:
            print("Fin de la ejecución")
            sys.exit(0)

# ===============================
#       Option functions
# ===============================

def findClusters(analyzer: dict):
    """
    REQ 1
    User input, process and output to find clusters in connections
    graph

    Args
    -----
    analyzer: dict -- analizador
    """
    # User input
    landing1Name = userInput(
        "Nombre del landing point 1 (Ej: Jakarta, Indonesia): ",
        validateMap=analyzer["landingsByName"],
        notFPromt="Nombre no encontrado, intente nuevamente")
    landing2Name = userInput(
        "Nombre del landing point 2 (Ej: Singapore, Singapore): ",
        validateMap=analyzer["landingsByName"],
        notFPromt="Nombre no encontrado, intente nuevamente")
    # Process
    ans = controller.findClusters(analyzer, landing1Name, landing2Name)
    # Output
    print("El total de componentes fuertemente conectados es:", ans["components"])
    if ans["stronglyC"]:
        print("Los landing points se encuentran fuertemente conectados")
    else:
        print("Los landing points NO se encuentran fuertemente conectados")
    eoc()
    # Map
    # TODO encontrar ruta entre los dos vertices
    print("Creando mapa...")
    gMap = geoMap.newFullMap()
    geoMap.addVertex(analyzer, gMap, ans["vertexA"])
    geoMap.addVertex(analyzer, gMap, ans["vertexB"])
    geoMap.showMap(gMap)
    print("Abriendo mapa...")


def minimunRoute(analyzer: dict):
    """
    REQ 2
    User input, process and output to find the minimun route
    between two country capitals.

    Args
    ----
    analyzer: dict -- analizador
    """
    # Input
    countryName1 = userInput(
        "Ingrese el nombre del país 1 (ej. Belgium): ",
        validateMap=analyzer["countries"],
        notFPromt="País no encontrado, intente nuevamente"
    )
    countryName2 = userInput(
        "Ingrese el nombre del país 2 (ej. Germany): ",
        validateMap=analyzer["countries"],
        notFPromt="País no encontrado, intente nuevamente"
    )
    # Process
    print("Cargando...")
    ans = controller.minimumRoute(analyzer, countryName1, countryName2)
    # Output
    # Si no hay ruta
    if ans["status"] == 0:
        print("No se encontró una ruta entre las capitales de los dos paises")
        eoc()
        return
    # Si hay ruta
    routeLen = lt.size(ans["path"])
    print("La ruta es de longitud", routeLen)
    print("A continuación se mostrará la ruta en un mapa.")
    eoc()
    # Map
    print("Creando mapa...")
    gMap = geoMap.newFullMap()
    geoMap.addEdges(analyzer, gMap, ans["path"], True)
    geoMap.showMap(gMap)
    print("Abriendo mapa...")
    print()


def minimumSpanNet(analyzer: dict):
    """
    REQ 3
    User input, process and output to find the minimum span
    tree of connections graph

    Args
    ----
    analyzer: dict -- analizador
    """
    # Process
    print("Cargando...")
    ans = controller.minimumSpanNet(analyzer)
    # Crea un mapa vacio
    gMap = geoMap.newFullMap()
    # Obtiene la lista de vertices del MST
    verticesLst = mp.keySet(ans["MST"]["marked"])
    # Número de vertices en el MST
    vertexCnt = 0
    # Inicializa la variable totalCost
    totalCost = 0
    for vertex in lt.iterator(verticesLst):
        # Añade el vertice al mapa
        if vertex == ans["orVertex"]:
            geoMap.addVertex(analyzer, gMap, vertex, "red")
        else:
            geoMap.addVertex(analyzer, gMap, vertex)
            
        # Obtiene el arco asociado al vertice
        edgeTo = getMapValue(ans["MST"]["edgeTo"], vertex)
        if not edgeTo is None:
            # Suma el costo del arco al costo total del MST
            totalCost += edgeTo["weight"]
            # Suma 1 al número de vertices conectados
            vertexCnt += 1
            # Añade el arco al mapa
            geoMap.addEdge(analyzer, gMap, edgeTo)
    # Output
    print("\nVertice de origen:", ans["orVertex"])
    print("Número de vertices conectados:", vertexCnt)
    print("Costo total del MST:", round(totalCost, 2), " km")
    #TODO ramam mas larga
    print("A continuación se mostrará el mapa con el MST.")
    eoc()
    print("Cargando mapa...")
    geoMap.showMap(gMap)
    print("Abriendo mapa...")
# ============================
#       Otras funciones
# ============================

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


"""
MAIN PROGRAM
"""
if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=init)
    thread.start()