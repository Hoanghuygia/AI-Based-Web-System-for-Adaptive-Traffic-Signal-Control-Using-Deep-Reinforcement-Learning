import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Data directory
DATA_DIR = os.path.join(BASE_DIR, 'data')

MAP_DIR = os.path.join(DATA_DIR, 'map')
DISTRICT_1_OSM = os.path.join(MAP_DIR, 'region_1.osm')
DISTRICT_1_TRAFFIC_CHART = os.path.join(MAP_DIR, 'region_1_network.png')
# SUMO directory
SUMO_DIR = os.path.join(BASE_DIR, 'sumo_files')

NETWORK_DIR = os.path.join(SUMO_DIR, 'network')
DISTRICT_1_NET = os.path.join(NETWORK_DIR, 'region_1.net.xml')