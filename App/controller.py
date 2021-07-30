﻿"""
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
    firstLanding    =   loadLandings(analyzer)
    loadConnections(analyzer)
    lastCountry     =   loadCountries(analyzer)
    # Conecta los vertices que tienen un landing común
    model.groupLandings(analyzer)

    returnDict = {
        "firstLanding": firstLanding,
        "lastCountry": lastCountry
    }

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


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
