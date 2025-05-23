import xml.etree.ElementTree as ET
import pandas as pd
from pyproj import Transformer
import os

def calc_dist(x1, y1, x2, y2):
    """
    Calculate Euclidean distance between two points.
    
    Args:
        x1, y1 (float): Coordinates of the first point
        x2, y2 (float): Coordinates of the second point
        
    Returns:
        float: Euclidean distance
    """
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def extract_junctions(net_file_path):
    """
    Extract junction information from a SUMO .net.xml file.
    
    Args:
        net_file_path (str): Path to the .net.xml file
        
    Returns:
        list: List of dictionaries containing junction information
    """
    # Check if file exists
    if not os.path.exists(net_file_path):
        raise FileNotFoundError(f"File {net_file_path} not found")
    
    # Parse the XML file
    tree = ET.parse(net_file_path)
    root = tree.getroot()
    
    junctions = []
    
    # Extract junction information
    for junction in root.findall('.//junction'):
        junction_id = junction.get('id')
        
        # Skip internal junctions (those with ":" in their ID)
        if ":" in junction_id:
            continue
        
        # Check if junction has valid coordinates
        if junction.get('x') is None or junction.get('y') is None:
            continue
            
        x = float(junction.get('x'))
        y = float(junction.get('y'))
        junction_type = junction.get('type', '')
        incLanes = junction.get('incLanes', '')
        intLanes = junction.get('intLanes', '')
        shape = junction.get('shape', '')
        
        junction_info = {
            'id': junction_id,
            'x': x,
            'y': y,
            'type': junction_type,
            'incLanes': incLanes,
            'intLanes': intLanes,
            'shape': shape
        }
        
        junctions.append(junction_info)
    
    return junctions

def find_closest_junction(junctions, x_utm, y_utm):
    """
    Find the closest junction to the given coordinates.
    
    Args:
        junctions (list): List of junction dictionaries
        x_utm, y_utm (float): UTM coordinates adjusted with netOffset
        
    Returns:
        str or None: ID of the closest junction, or None if no junction is found
    """
    min_dist = float('inf')
    closest_junction_id = None
    
    for junction in junctions:
        x_junction, y_junction = junction['x'], junction['y']
        dist = calc_dist(x_utm, y_utm, x_junction, y_junction)
        if dist < min_dist:
            min_dist = dist
            closest_junction_id = junction['id']
    
    return closest_junction_id

if __name__ == "__main__":
    net_file = "src/model/sumo_files/network/region_1.net.xml"
    intersection_file = "src/model/data/intersections/intersection_list.csv"
    output_file = "src/model/data/intersections/intersection_mapping.csv"  # File to save mapping results

    # Check if input files exist
    if not os.path.exists(net_file):
        raise FileNotFoundError(f"Network file {net_file} not found")
    if not os.path.exists(intersection_file):
        raise FileNotFoundError(f"Intersection file {intersection_file} not found")

    # Extract netOffset from .net.xml
    tree = ET.parse(net_file)
    root = tree.getroot()
    location = root.find('.//location')
    if location is None:
        raise ValueError("No <location> tag found in .net.xml")
    
    net_offset = location.get('netOffset').split(',')
    offset_x, offset_y = float(net_offset[0]), float(net_offset[1])
    print("Offset x: ", offset_x)
    print("Offset y: ", offset_y)

    # Extract junctions
    junctions = extract_junctions(net_file)
    # print(junctions)
    print('----------------------------------------------------------')

    # Create transformer from WGS84 (EPSG:4326) to UTM zone 48N
    transformer = Transformer.from_crs("EPSG:4326", "+proj=utm +zone=48 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

    # Read intersection CSV file
    df = pd.read_csv(intersection_file)

    # Convert lat, lng to UTM coordinates
    def convert_row(row):
        x, y = transformer.transform(row['lat'], row['lng'])
        return pd.Series({'x': x, 'y': y})

    utm_coords = df.apply(convert_row, axis=1)
    df = pd.concat([df, utm_coords], axis=1)

    # Adjust coordinates with netOffset
    intersection_coords = {
        row['name']: {
            'lat': row['lat'],
            'lng': row['lng'],
            'x': row['x'] + offset_x,
            'y': row['y'] + offset_y
        }
        for _, row in df.iterrows()
    }
    print(intersection_coords)
    print("-----------------------------------------------------------")

    # Map intersections to junctions
    intersection_mapping = {}
    for name, coords in intersection_coords.items():
        junction_id = find_closest_junction(junctions, coords['x'], coords['y'])
        if junction_id:
            intersection_mapping[name] = junction_id
        else:
            print(f"[WARNING] No junction found for intersection {name}")

    # Save mapping to CSV
    mapping_df = pd.DataFrame(list(intersection_mapping.items()), columns=['Intersection', 'Junction_ID'])
    mapping_df.to_csv(output_file, index=False)
    print(f"Mapping saved to {output_file}")