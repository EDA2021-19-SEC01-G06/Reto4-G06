import os
import folium
import subprocess
import platform
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
import controller

# Set up
global_dir = os.path.join(os.path.dirname(__file__), '..')
local_dir = os.path.dirname(__file__)
temp_folder = os.path.join(global_dir, "temp")
map_path = os.path.join(temp_folder, "map.html")

# Map creation
def newFullMap():
    return folium.Map([40, 0], zoom_start=2)

def addEdges(analyzer: dict, m: folium.Map, edgeList):
    """
    Añade arcos del grafo connections al mapa, en forma de lineas

    Args
    ----
    analyzer: dict -- analizador
    m: folium.Map -- objeto de tipo folium.Map
    edgeList -- TAD lista con la lista de los arcos
    """
    for edge in lt.iterator(edgeList):
        landingA = controller.getLanFromVer(analyzer, edge["vertexA"])
        landingB = controller.getLanFromVer(analyzer, edge["vertexB"])
        cableName = edge["vertexA"].split("-")[1]
        weight = str(edge["weight"])
        orgDest = landingA["landing_point_id"]  + " &rarr; " + landingB["landing_point_id"]
        popup = "." * 40 + "<br>" + "Cable: " + cableName + "<br>" + "Distance: " + weight + " km<br>" + \
        orgDest
        latLonA = (float(landingA["latitude"]), float(landingA["longitude"]))
        latLonB = (float(landingB["latitude"]), float(landingB["longitude"]))
        folium.PolyLine([latLonA, latLonB], popup).add_to(m)


def addVertices(analyzer: dict, m: folium.Map, verticesLst):
    """
    Añade vertices del grafo connections al mapa, en forma de marcadores

    Args
    ----
    analyzer: dict -- analizador
    m: folium.Map -- objeto de tipo folium.Map
    verticesLst -- TAD lista con lista de vertices a añadir
    """
    for vertex in lt.iterator(verticesLst):
        landing = controller.getLanFromVer(analyzer, vertex)
        cableName = vertex.split("-")[1]
        popup = "." * 40 + "<br>Id: " + landing["landing_point_id"] + "<br>" + \
            "Name: " + landing["name"]
        latLon = (float(landing["latitude"]), float(landing["longitude"]))
        folium.Marker(latLon, popup).add_to(m)


def showMap(m: folium.Map):
    """
    Abre el mapa en el navegador por defecto del sistema.

    Args
    ----
    m: folium.Map -- Objeto de tipo folium.Map
    """
    global map_path
    m.save(map_path)
    openMap()


def openMap(path = None):

    try:
        if path is None:
            global map_path
            path = map_path

        if platform.system().lower() == "darwin":            # macOs
            subprocess.call(('open', path))
        elif platform.system().lower() == "windows":        # Windows
            os.startfile(path)
        else:                                               # Linux variants
            subprocess.call(('xdg-open', path))
    except:
        print("Error intentando abrir el archivo.")
        print("Por favor abra el mapa manualmente desde", map_path)