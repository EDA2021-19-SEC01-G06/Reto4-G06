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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

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


def mainMenu(analyzer):
    """
    Ciclo. Menú principal.
    """
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            pass
        elif int(inputs[0]) == 2:
            pass
        else:
            sys.exit(0)


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
    print("\nLanding points cargados:", mp.size(analyzer["landings"]))
    print("Conecciones cargadas:", gr.numEdges(analyzer["connectionsGr"]))
    print("Paises cargados:", mp.size(analyzer["countries"]))
    print()
    controller.mtt.printTrace()
    print()
    eoc()
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



"""
MAIN PROGRAM
"""
try:
    init()
    sys.exit(0)
except RecursionError:
    print("***MÁXIMA RECURCIÓN ALCANZADA***")
    crnt_rec_limit = sys.getrecursionlimit()
    new_rec_limit = crnt_rec_limit * 10
    print("El límite actual es de", crnt_rec_limit)
    print("Ahora el programa se ejecutará con un límite de", new_rec_limit)
    eoc()
    init()