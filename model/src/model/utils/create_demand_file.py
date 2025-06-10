import xml.etree.ElementTree as ET
import pandas as pd
import sumolib
import os
import numpy as np
from datetime import datetime
import glob

def define_vehicle_types(routes):
    """
    Define vehicle types (vType) for .rou.xml file, based on HCMC traffic.
    Adjusted to simulate lane invasion, aggressive lane changing, and cutting in.
    """
    vtypes = [
        {
            "id": "motorcycle",
            "vClass": "motorcycle",
            "accel": "3.0",
            "decel": "5.0",
            "sigma": "0.7",
            "length": "2.0",
            "width": "0.8",
            "maxSpeed": "16.67",
            "color": "yellow",
            "minGap": "0.5",
            "lcAssertive": "1.6",
            "lcSpeedGain": "1.6",
            "lcStrategic": "1.3",
            "lcCooperative": "0.7"
        },
        {
            "id": "car",
            "vClass": "passenger",
            "accel": "2.5",
            "decel": "4.5",
            "sigma": "0.3",
            "length": "4.5",
            "width": "1.8",
            "maxSpeed": "13.89",
            "color": "blue",
            "minGap": "2.0",
            "lcAssertive": "1.2",
            "lcSpeedGain": "1.3",
            "lcStrategic": "1.6",
            "lcCooperative": "0.8"
        },
        {
            "id": "bus",
            "vClass": "bus",
            "accel": "1.5",
            "decel": "3.5",
            "sigma": "0.2",
            "length": "12.0",
            "width": "2.5",
            "maxSpeed": "11.11",
            "color": "green",
            "minGap": "3.0",
            "lcAssertive": "1.0",
            "lcSpeedGain": "1.0",
            "lcStrategic": "1.0",
            "lcCooperative": "1.0"
        },
        {
            "id": "truck",
            "vClass": "truck",
            "accel": "1.8",
            "decel": "4.0",
            "sigma": "0.2",
            "length": "7.5",
            "width": "2.2",
            "maxSpeed": "11.11",
            "color": "red",
            "minGap": "3.0",
            "lcAssertive": "1.0",
            "lcSpeedGain": "1.0",
            "lcStrategic": "1.0",
            "lcCooperative": "1.0"
        }
    ]
    for vtype in vtypes:
        ET.SubElement(routes, "vType", **vtype)
    # print("[INFO] Defined vehicle types with adjusted lane-changing behavior")

def get_route_info(net, route_id, routes):
    """
    Get width and road type information from a route in the SUMO network.
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
        route_type = max(set(edge_types), key=edge_types.count)
        return avg_width, route_type
    except Exception as e:
        # print(f"[WARNING] Failed to get route info for {route_id}: {e}. Using defaults.")
        return 4.0, "highway.secondary"

def estimate_vehicle_counts(traffic_condition, distance_meters, duration_seconds, route_id, routes, net):
    """
    Estimate the number of vehicles per hour based on traffic density, distance, speed,
    road width, and road type.
    """
    try:
        base_density = {
            'normal': {'motorcycle': 50, 'car': 10, 'bus': 1, 'truck': 0.5},
            'moderate': {'motorcycle': 100, 'car': 15, 'bus': 2, 'truck': 1},
            'heavy': {'motorcycle': 150, 'car': 20, 'bus': 3, 'truck': 1.5}
        }
        density = base_density.get(traffic_condition.lower(), base_density['normal'])
        
        route_width, route_type = get_route_info(net, route_id, routes)
        scale_width = min(2.0, route_width / 4.0)
        scale_type = 1.5 if "primary" in route_type else 0.5 if "residential" in route_type else 1.0
        speed = (distance_meters / max(duration_seconds, 1)) * 3.6
        speed = max(5.0, min(speed, 40.0))
        
        counts = {k: int(v * scale_width * scale_type * speed) for k, v in density.items()}
        max_flow = {'motorcycle': 1000, 'car': 300, 'bus': 20, 'truck': 15}
        counts = {k: min(v, max_flow[k]) for k, v in counts.items()}
        
        return counts
    except Exception as e:
        # print(f"[ERROR] Failed to estimate vehicle counts: {e}. Using default.")
        return {'motorcycle': 300, 'car': 50, 'bus': 5, 'truck': 3}

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
        if from_node == to_node:
            # print(f"[WARNING] Skipping route from {from_node} to {to_node}: same node")
            return None
            
        # Check if nodes exist
        if not net.hasNode(from_node) or not net.hasNode(to_node):
            # print(f"[ERROR] Node {from_node} or {to_node} not found in network")
            return None
            
        # Try getShortestPath first
        try:
            path = net.getShortestPath(net.getNode(from_node), net.getNode(to_node))[0]
            if path:
                edges = [edge.getID() for edge in path]
                route_id = f"route_{vehicle_id}"
                ET.SubElement(routes, "route", id=route_id, edges=" ".join(edges))
                # print(f"[INFO] Found route {route_id} from {from_node} to {to_node}")
                return route_id
        except Exception as e:
            # print(f"[WARNING] getShortestPath failed for {from_node} to {to_node}: {e}")
            a = 1 + 1
        
        # Fallback: Manual path finding using BFS
        from sumolib.net import Net
        visited = set()
        queue = [(from_node, [from_node])]
        while queue:
            current_node, path = queue.pop(0)
            if current_node == to_node:
                # Convert node path to edge path
                edges = []
                for i in range(len(path) - 1):
                    from_junction = net.getNode(path[i])
                    to_junction = net.getNode(path[i + 1])
                    for edge in from_junction.getOutgoing():
                        if edge.getToNode().getID() == to_junction.getID():
                            edges.append(edge.getID())
                            break
                if edges:
                    route_id = f"route_{vehicle_id}"
                    ET.SubElement(routes, "route", id=route_id, edges=" ".join(edges))
                    # print(f"[INFO] Found fallback route {route_id} from {from_node} to {to_node}")
                    return route_id
                continue
                
            if current_node in visited:
                continue
            visited.add(current_node)
            
            current_junction = net.getNode(current_node)
            for edge in current_junction.getOutgoing():
                next_node = edge.getToNode().getID()
                if next_node not in visited:
                    queue.append((next_node, path + [next_node]))
        
        # print(f"[WARNING] No path found from {from_node} to {to_node}")
        return None
        
    except Exception as e:
        print(f"[ERROR] Failed to find route from {from_node} to {to_node}: {e}")
        return None

def create_flows(routes, net, traffic_data, intersection_mapping, simulation_period):
    """
    Create flows for .rou.xml file based on traffic data.
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
                        # print(f"[WARNING] Skipping {origin} to {destination}: not in intersection mapping")
                        continue
                    
                    from_node = intersection_mapping[origin]
                    to_node = intersection_mapping[destination]
                    
                    route_id = find_route(net, from_node, to_node, vehicle_id, routes)
                    if not route_id:
                        continue
                    
                    counts = estimate_vehicle_counts(
                        row['traffic_condition'],
                        row['distance_meters'],
                        row['duration_seconds'],
                        route_id,
                        routes,
                        net
                    )
                    
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
                            
        # print(f"[INFO] Created {vehicle_id} flows")
    except Exception as e:
        print(f"[ERROR] Failed to create flows: {e}")

# def create_route_file(net_file, traffic_data_files, mapping_file, output_file, simulation_period=259200):
#     """
#     Create .rou.xml file from traffic flow data using pre-defined intersection mapping.
#     """
#     try:
#         net = sumolib.net.readNet(net_file)
#         traffic_data = pd.concat([pd.read_csv(f) for f in traffic_data_files], ignore_index=True)
        
#         mapping_df = pd.read_csv(mapping_file)
#         intersection_mapping = {row['Intersection']: str(row['Junction_ID']) for _, row in mapping_df.iterrows()}
        
#         print(f"Intersection mapping: {intersection_mapping}")
#         print(f"Unique nodes: {len(set(intersection_mapping.values()))}")
        
#         if not intersection_mapping:
#             print("[ERROR] Intersection mapping is empty. Check mapping_file.")
#             return
#         if len(set(intersection_mapping.values())) < 2:
#             print(f"[ERROR] Only {len(set(intersection_mapping.values()))} unique node(s). Need at least 2 for routes.")
#             return
        
#         routes = ET.Element("routes")
#         define_vehicle_types(routes)
#         create_flows(routes, net, traffic_data, intersection_mapping, simulation_period)
        
#         tree = ET.ElementTree(routes)
#         os.makedirs(os.path.dirname(output_file), exist_ok=True)
#         tree.write(output_file, encoding="utf-8", xml_declaration=True)
#         print(f"[INFO] Created route file: {output_file}")
        
#     except Exception as e:
#         print(f"[ERROR] Failed to create route file: {e}")

def create_route_file(net_file, traffic_data_files, mapping_file, output_file, simulation_period=259200):
    """
    Create .rou.xml file from traffic flow data using pre-defined intersection mapping.
    """
    try:
        print(f"[DEBUG] Loading network file: {net_file}")
        net = sumolib.net.readNet(net_file)
        
        # DEBUG: Kiểm tra network
        all_nodes = [node.getID() for node in net.getNodes()]
        print(f"[DEBUG] Network has {len(all_nodes)} nodes")
        print(f"[DEBUG] Sample nodes: {all_nodes[:5]}")
        
        # Load data
        traffic_data = pd.concat([pd.read_csv(f) for f in traffic_data_files], ignore_index=True)
        mapping_df = pd.read_csv(mapping_file)
        intersection_mapping = {row['Intersection']: str(row['Junction_ID']) for _, row in mapping_df.iterrows()}
        
        # DEBUG: Kiểm tra mapping
        print(f"[DEBUG] Intersection mapping: {intersection_mapping}")
        
        # Kiểm tra nodes có tồn tại không
        valid_mapping = {}
        for intersection, node_id in intersection_mapping.items():
            if node_id in all_nodes:
                valid_mapping[intersection] = node_id
                print(f"[✓] {intersection} -> {node_id} OK")
            else:
                print(f"[✗] {intersection} -> {node_id} NOT FOUND")
        
        if len(valid_mapping) < 2:
            print(f"[ERROR] Only {len(valid_mapping)} valid nodes found. Need at least 2.")
            return
        
        print(f"[INFO] Using {len(valid_mapping)} valid intersections")
        
        # Tiếp tục với valid_mapping thay vì intersection_mapping
        routes = ET.Element("routes")
        define_vehicle_types(routes)
        create_flows(routes, net, traffic_data, valid_mapping, simulation_period)  # Dùng valid_mapping
        
        tree = ET.ElementTree(routes)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"[INFO] Created route file: {output_file}")
        
    except Exception as e:
        print(f"[ERROR] Failed to create route file: {e}")
        
        