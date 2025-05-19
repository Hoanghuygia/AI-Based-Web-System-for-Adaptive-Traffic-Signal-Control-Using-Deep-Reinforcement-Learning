import xml.etree.ElementTree as ET
import pandas as pd
import sumolib
import os
import numpy as np
from datetime import datetime
from pyproj import Transformer

def define_vehicle_types(routes):
    """
    Define vehicle types (vType) for .rou.xml file, based on HCMC traffic.
    Adjusted to simulate lane invasion, aggressive lane changing, and cutting in.
    
    Args:
        routes: ElementTree root of .rou.xml file
    """
    vtypes = [
        {
            "id": "motorcycle",
            "vClass": "motorcycle",
            "accel": "3.0",
            "decel": "5.0",
            "sigma": "0.7",  # Increased to simulate random lane invasion and cutting in
            "length": "2.0",
            "width": "0.8",
            "maxSpeed": "16.67",  # 60 km/h
            "color": "yellow",
            "minGap": "0.5",  # Keep narrow gap for cutting in
            "lcAssertive": "1.6",  # Aggressive when changing lanes
            "lcSpeedGain": "1.6",  # Prioritize lane changing for faster speed
            "lcStrategic": "1.3",  # Prepare to change lanes early
            "lcCooperative": "0.7"  # Less cooperative, more cutting in
        },
        {
            "id": "car",
            "vClass": "passenger",
            "accel": "2.5",
            "decel": "4.5",
            "sigma": "0.3",  # Slightly random, but less than motorcycles
            "length": "4.5",
            "width": "1.8",
            "maxSpeed": "13.89",  # 50 km/h
            "color": "blue",
            "minGap": "2.0",  # Slightly reduced to allow closer overtaking
            "lcAssertive": "1.2",  # Cautious lane changing but still overtakes
            "lcSpeedGain": "1.3",  # Overtakes when the adjacent lane is faster
            "lcStrategic": "1.6",  # Prepare to change lanes early
            "lcCooperative": "0.8"  # More cooperative than motorcycles
        },
        {
            "id": "bus",
            "vClass": "bus",
            "accel": "1.5",
            "decel": "3.5",
            "sigma": "0.2",  # Stable, less lane invasion
            "length": "12.0",
            "width": "2.5",
            "maxSpeed": "11.11",  # 40 km/h
            "color": "green",
            "minGap": "3.0",
            "lcAssertive": "1.0",  # Normal, less lane changing
            "lcSpeedGain": "1.0",  # Less overtaking
            "lcStrategic": "1.0",  # Normal
            "lcCooperative": "1.0"  # Normal cooperation
        },
        {
            "id": "truck",
            "vClass": "truck",
            "accel": "1.8",
            "decel": "4.0",
            "sigma": "0.2",  # Stable, less lane invasion
            "length": "7.5",
            "width": "2.2",
            "maxSpeed": "11.11",  # 40 km/h
            "color": "red",
            "minGap": "3.0",
            "lcAssertive": "1.0",  # Normal, less lane changing
            "lcSpeedGain": "1.0",  # Less overtaking
            "lcStrategic": "1.0",  # Normal
            "lcCooperative": "1.0"  # Normal cooperation
        }
    ]
    for vtype in vtypes:
        ET.SubElement(routes, "vType", **vtype)
    print("[INFO] Defined vehicle types with adjusted lane-changing behavior")

def get_route_info(net, route_id, routes):
    """
    Get width and road type information from a route in the SUMO network.
    
    Args:
        net: SUMO network (sumolib.net.readNet)
        route_id: ID of the route
        routes: ElementTree root of .rou.xml file
    
    Returns:
        tuple: (average width (m), road type (str))
    """
    try:
        route = routes.find(f"route[@id='{route_id}']")
        if route is None:
            raise ValueError(f"Route {route_id} not found")
        edges = route.get("edges").split()
        total_width = 0
        edge_types = []
        for edge_id in edges:
            edge = net.getEdge(edge_id)
            total_width += edge.getWidth()
            edge_type = edge.getType() or "highway.secondary"
            edge_types.append(edge_type)
        avg_width = total_width / len(edges)
        # Choose the most common road type
        route_type = max(set(edge_types), key=edge_types.count)
        return avg_width, route_type
    except Exception as e:
        print(f"[WARNING] Failed to get route info for {route_id}: {e}. Using defaults.")
        return 4.0, "highway.secondary"

def estimate_vehicle_counts(traffic_condition, distance_meters, duration_seconds, route_id, routes, net):
    """
    Estimate the number of vehicles per hour based on traffic density, distance, speed,
    road width, and road type.
    
    Args:
        traffic_condition (str): normal, moderate, heavy
        distance_meters (float): Distance between two intersections
        duration_seconds (float): Travel time
        route_id (str): ID of the route
        routes: ElementTree root of .rou.xml file
        net: SUMO network
    
    Returns:
        dict: Number of motorcycles, cars, buses, trucks per hour
    """
    try:
        # Base density (vehicles/km) based on Jakarta (Transportation Research Procedia, 2020)
        base_density = {
            'normal': {'motorcycle': 50, 'car': 10, 'bus': 1, 'truck': 0.5},
            'moderate': {'motorcycle': 100, 'car': 15, 'bus': 2, 'truck': 1},
            'heavy': {'motorcycle': 150, 'car': 20, 'bus': 3, 'truck': 1.5}
        }
        density = base_density.get(traffic_condition.lower(), base_density['normal'])
        
        # Get road width and type
        route_width, route_type = get_route_info(net, route_id, routes)
        
        # Adjust based on width (4m is standard)
        scale_width = min(2.0, route_width / 4.0)  # Increase up to 2x for wide roads
        # Adjust based on road type
        scale_type = 1.5 if "primary" in route_type else 0.5 if "residential" in route_type else 1.0
        # Calculate speed (km/h) from duration_seconds
        speed = (distance_meters / max(duration_seconds, 1)) * 3.6  # m/s to km/h
        speed = max(5.0, min(speed, 40.0))  # Limit speed to 5-40 km/h
        
        # Convert density to flow (vehicles/hour = vehicles/km × km/h)
        counts = {k: int(v * scale_width * scale_type * speed) for k, v in density.items()}
        
        # Maximum flow limits (based on Jakarta and Hanoi)
        max_flow = {'motorcycle': 1000, 'car': 300, 'bus': 20, 'truck': 15}
        counts = {k: min(v, max_flow[k]) for k, v in counts.items()}
        
        return counts
    except Exception as e:
        print(f"[ERROR] Failed to estimate vehicle counts: {e}. Using default.")
        return {'motorcycle': 300, 'car': 50, 'bus': 5, 'truck': 3}

def find_closest_node(net, lat, lng):
    """
    Find the closest node in the SUMO network based on lat, lng coordinates.
    
    Args:
        net: SUMO network
        lat, lng: Intersection coordinates (WGS84, degrees)
    
    Returns:
        str: ID of the closest node or None if not found
    """
    try:
        # Chuyển đổi lat, lng từ WGS84 sang UTM zone 48N
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:32648")  # WGS84 to UTM 48N
        x_utm, y_utm = transformer.transform(lat, lng)
        
        # Áp dụng netOffset từ region_1.net.xml
        net_offset_x, net_offset_y = -684826.81, -1192114.63
        x_input = x_utm - net_offset_x  # Tọa độ tương đối trong hệ SUMO
        y_input = y_utm - net_offset_y
        
        min_dist = float('inf')
        closest_node = None
        for node in net.getNodes():
            x, y = node.getCoord()  # Tọa độ trong hệ SUMO (mét, sau offset)
            dist = ((x_input - x) ** 2 + (y_input - y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_node = node.getID()
        return closest_node
    except Exception as e:
        print(f"[ERROR] Failed to find closest node for lat={lat}, lng={lng}: {e}")
        return None

def find_route(net, from_node, to_node, vehicle_id, routes):
    """
    Find the shortest path between two nodes and add the route to the .rou.xml file.
    
    Args:
        net: SUMO network
        from_node, to_node: IDs of source and destination nodes
        vehicle_id: ID to create a unique route
        routes: ElementTree root of .rou.xml file
    
    Returns:
        str: ID of the route or None if not found
    """
    try:
        path = net.getShortestPath(net.getNode(from_node), net.getNode(to_node))[0]
        if not path:
            print(f"[WARNING] No path from {from_node} to {to_node}")
            return None
        edges = [edge.getID() for edge in path]
        route_id = f"route_{vehicle_id}"
        ET.SubElement(routes, "route", id=route_id, edges=" ".join(edges))
        return route_id
    except Exception as e:
        print(f"[ERROR] Failed to find route from {from_node} to {to_node}: {e}")
        return None

def create_flows(routes, net, traffic_data, intersection_mapping, simulation_period):
    """
    Create flows for .rou.xml file based on traffic data.
    
    Args:
        routes: ElementTree root
        net: SUMO network
        traffic_data: DataFrame containing traffic data
        intersection_mapping: Dict mapping intersection names to node IDs
        simulation_period: Simulation time (seconds)
    """
    vehicle_id = 0
    hours_to_check = [7, 9, 12, 17, 19, 22]
    
    try:
        unique_days = traffic_data['day_of_week'].unique()
        for day_idx, day in enumerate(unique_days):
            day_data = traffic_data[traffic_data['day_of_week'] == day]
            base_date = datetime(2025, 5, 14)
            day_offset = (day - 2) % 7
            sim_day_start = day_idx * 86400
            
            for hour in hours_to_check:
                hour_data = day_data[day_data['hour_of_day'] == hour]
                begin_time = sim_day_start + hour * 3600
                end_time = begin_time + 3600
                
                for idx, row in hour_data.iterrows():
                    origin = row['origin']
                    destination = row['destination']
                    
                    if origin not in intersection_mapping or destination not in intersection_mapping:
                        print(f"[WARNING] Skipping {origin} to {destination}: not in intersection mapping")
                        continue
                    
                    from_node = intersection_mapping[origin]
                    to_node = intersection_mapping[destination]
                    
                    route_id = find_route(net, from_node, to_node, vehicle_id, routes)
                    if not route_id:
                        continue
                    
                    # Estimate flow based on density
                    counts = estimate_vehicle_counts(
                        row['traffic_condition'],
                        row['distance_meters'],
                        row['duration_seconds'],
                        route_id,
                        routes,
                        net
                    )
                    
                    # Create flow for each vehicle type
                    for vtype, count in counts.items():
                        if count > 0:
                            flow = ET.SubElement(
                                routes,
                                "flow",
                                id=f"flow_{vtype}_{vehicle_id}",
                                type=vtype,
                                begin=str(begin_time),
                                end=str(end_time),
                                vehsPerHour=str(count),
                                route=route_id
                            )
                            vehicle_id += 1
                            
        print(f"[INFO] Created {vehicle_id} flows")
    except Exception as e:
        print(f"[ERROR] Failed to create flows: {e}")

def create_route_file(net_file, traffic_data_files, intersection_file, output_file, simulation_period=259200):
    """
    Create .rou.xml file from traffic flow data.
    
    Args:
        net_file: Path to .net.xml file
        traffic_data_files: List of traffic CSV files
        intersection_file: CSV file containing intersection coordinates
        output_file: Path to .rou.xml file
        simulation_period: Simulation time (seconds, default: 3 days)
    """
    try:
        net = sumolib.net.readNet(net_file)
        traffic_data = pd.concat([pd.read_csv(f) for f in traffic_data_files], ignore_index=True)
        intersections_df = pd.read_csv(intersection_file)
        intersection_coords = {
            row['name']: {'lat': row['lat'], 'lng': row['lng']}
            for _, row in intersections_df.iterrows()
        }
        
        intersection_mapping = {}
        for name, coords in intersection_coords.items():
            node_id = find_closest_node(net, coords['lat'], coords['lng'])
            if node_id:
                intersection_mapping[name] = node_id
            else:
                print(f"[WARNING] No node found for intersection {name}")
        
        routes = ET.Element("routes")
        define_vehicle_types(routes)
        create_flows(routes, net, traffic_data, intersection_mapping, simulation_period)
        
        tree = ET.ElementTree(routes)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"[INFO] Created route file: {output_file}")
        
    except Exception as e:
        print(f"[ERROR] Failed to create route file: {e}")

if __name__ == "__main__":
    traffic_data_files = [
        "src/model/data/traffic/traffic_data_wednesday_2025-05-14.csv"
        "src/model/data/traffic/traffic_data_thursday_2025-05-15.csv"
        "src/model/data/traffic/traffic_data_friday_2025-05-16.csv"
    ]
    create_route_file(
        net_file="src/model/sumo_files/network/region_1.net.xml",
        traffic_data_files=traffic_data_files,
        intersection_file="src/model/data/traffic/intersection_list.csv",
        output_file="src/model/sumo_files/routes/region_1.rou.xml",
        simulation_period=259200
    )