import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox
from shapely.geometry import Polygon


def download_map(coords_dict, file_path, visual_path):
    """
    Downloads a map from OSM based on a bounding box and saves it as an .osm file
    plus a visual image of the network.

    Parameters:
    ----------
    coords_dict : dict
        Dictionary containing the bounding box:
        {
            "min_lon": float,
            "min_lat": float,
            "max_lon": float,
            "max_lat": float
        }

    file_path : str
        Path to save the OSM file (e.g., "data/map/region.osm")

    visual_path : str
        Path to save the network visualization image (e.g., "data/map/region.png")
    """

    ox.settings.all_oneway = True

    # Create a polygon from the bounding box
    bounding_box = [
        (coords_dict["min_lon"], coords_dict["min_lat"]),
        (coords_dict["min_lon"], coords_dict["max_lat"]),
        (coords_dict["max_lon"], coords_dict["max_lat"]),
        (coords_dict["max_lon"], coords_dict["min_lat"]),
    ]

    poly = Polygon(bounding_box)
    if not poly.is_valid:
        raise ValueError("Invalid Polygon.")

    gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[poly])

    try:
        # Download the road network graph
        G = ox.graph_from_polygon(
            gdf.loc[0, "geometry"], network_type="drive", simplify=False
        )
    except Exception as e:
        print(f"Error downloading graph: {e}")
        raise

    # Save the OSM file
    ox.save_graph_xml(G, filepath=file_path)

    # Plot and save the visualization
    fig, ax = plt.subplots(figsize=(12, 10))
    ox.plot_graph(
        G,
        ax=ax,
        node_color="red",
        edge_color="blue",
        node_size=30,
        show=False,
        close=False,
    )
    plt.title("Traffic Network from Bounding Box")
    plt.savefig(visual_path, dpi=300)
    plt.close()

    print(f"✅ Saved OSM to {file_path}")
    print(f"✅ Saved visualization to {visual_path}")