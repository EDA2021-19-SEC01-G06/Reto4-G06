import os
import sys
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
    endeList -- TAD lista con la lista de los arcos
    """
    for edge in lt.iterator(edgeList):
        landingA = controller.getLanFromVer(analyzer, edge["vertexA"])
        landingB = controller.getLanFromVer(analyzer, edge["vertexB"])


def openMap(path = None):
    if path is None:
        global map_path
        path = map_path

    if platform.system().lower() == "darwin":            # macOs
        subprocess.call(('open', path))
    elif platform.system().lower() == "windows":        # Windows
        os.startfile(path)
    else:                                               # Linux variants
        subprocess.call(('xdg-open', path))