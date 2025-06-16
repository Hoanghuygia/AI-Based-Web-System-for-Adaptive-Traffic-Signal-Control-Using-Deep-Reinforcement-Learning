import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

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

GOOGLE_MAP_DIRECTIONS_API_KEY = os.environ.get("GOOGLE_MAP_DIRECTIONS_API_KEY")
BASE_GOOGLE_MAP_URL = "https://maps.googleapis.com/maps/api/directions/json"

WEEKDAY_MAP = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday"
}

TRAFFIC_DIR = os.path.join(DATA_DIR, 'traffic')
INTERSEC_DIR = os.path.join(DATA_DIR, 'intersections')
INTERSECTION_DATA_FILE = os.path.join(INTERSEC_DIR, 'intersection_list.csv')