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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


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
    #TODO


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