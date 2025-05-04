import os
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def download_map(savePath):
    # os.makedirs("data/map", exist_ok=True)
    ox.settings.all_oneway = True

    quan_1_coords = [
        (106.689806, 10.783667), 
        (106.693667, 10.787028), 
        (106.6983333, 10.7829445), 
        (106.695000, 10.779250)
    ]

    quan_1_poly = Polygon(quan_1_coords)
    if not quan_1_poly.is_valid:
        raise ValueError("Invalid Polygon.")

    gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[quan_1_poly])

    try:
        G = ox.graph_from_polygon(gdf.loc[0, 'geometry'], network_type='drive', simplify=False)
    except Exception as e:
        print(f"Error downloading graph: {e}")
        raise

    ox.save_graph_xml(G, filepath='src/model/data/map/region_1.osm')

    fig, ax = plt.subplots(figsize=(12, 10))
    ox.plot_graph(G, ax=ax, node_color='red', edge_color='blue', node_size=30, show=True, close=False)
    plt.title('Traffic Network of District 1 Area')
    # plt.savefig('src/model/data/map/region_1_network.png')
    plt.savefig(savePath)
    plt.show()
