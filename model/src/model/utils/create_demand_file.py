import xml.etree.ElementTree as ET
import pandas as pd
import sumolib
import os
import numpy as np
from datetime import datetime

def define_vehicle_types(routes):
    """
    Định nghĩa các loại phương tiện (vType) cho file .rou.xml, dựa trên giao thông HCMC.
    
    Args:
        routes: ElementTree root của file .rou.xml
    """
    vtypes = [
        {
            "id": "motorcycle",
            "vClass": "motorcycle",
            "accel": "3.0",
            "decel": "5.0",
            "sigma": "0.5",
            "length": "2.0",
            "width": "0.8",
            "maxSpeed": "16.67",  # 60 km/h
            "color": "yellow",
            "minGap": "0.5",
            "lcAssertive": "1.0"
        },
        {
            "id": "car",
            "vClass": "passenger",
            "accel": "2.5",
            "decel": "4.5",
            "sigma": "0.3",
            "length": "4.5",
            "width": "1.8",
            "maxSpeed": "13.89",  # 50 km/h
            "color": "blue",
            "minGap": "2.5"
        },
        {
            "id": "bus",
            "vClass": "bus",
            "accel": "1.5",
            "decel": "3.5",
            "sigma": "0.2",
            "length": "12.0",
            "width": "2.5",
            "maxSpeed": "11.11",  # 40 km/h
            "color": "green",
            "minGap": "3.0"
        },
        {
            "id": "truck",
            "vClass": "truck",
            "accel": "1.8",
            "decel": "4.0",
            "sigma": "0.3",
            "length": "7.5",
            "width": "2.2",
            "maxSpeed": "11.11",  # 40 km/h
            "color": "red",
            "minGap": "3.0"
        }
    ]
    for vtype in vtypes:
        ET.SubElement(routes, "vType", **vtype)
    print("[INFO] Defined vehicle types")

def get_route_info(net, route_id, routes):
    """
    Lấy thông tin độ rộng và loại đường từ route trong mạng SUMO.
    
    Args:
        net: Mạng SUMO (sumolib.net.readNet)
        route_id: ID của route
        routes: ElementTree root của file .rou.xml
    
    Returns:
        tuple: (trung bình độ rộng (m), loại đường (str))
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
        # Chọn loại đường phổ biến nhất
        route_type = max(set(edge_types), key=edge_types.count)
        return avg_width, route_type
    except Exception as e:
        print(f"[WARNING] Failed to get route info for {route_id}: {e}. Using defaults.")
        return 4.0, "highway.secondary"

def estimate_vehicle_counts(traffic_condition, distance_meters, duration_seconds, route_id, routes, net):
    """
    Ước tính số lượng phương tiện mỗi giờ dựa trên mật độ giao thông, khoảng cách, tốc độ,
    độ rộng đường, và loại đường.
    
    Args:
        traffic_condition (str): normal, moderate, heavy
        distance_meters (float): Khoảng cách giữa hai giao lộ
        duration_seconds (float): Thời gian di chuyển
        route_id (str): ID của route
        routes: ElementTree root của file .rou.xml
        net: Mạng SUMO
    
    Returns:
        dict: Số lượng xe máy, ô tô, xe buýt, xe tải mỗi giờ
    """
    try:
        # Mật độ cơ bản (xe/km) dựa trên Jakarta (Transportation Research Procedia, 2020)
        base_density = {
            'normal': {'motorcycle': 50, 'car': 10, 'bus': 1, 'truck': 0.5},
            'moderate': {'motorcycle': 100, 'car': 15, 'bus': 2, 'truck': 1},
            'heavy': {'motorcycle': 150, 'car': 20, 'bus': 3, 'truck': 1.5}
        }
        density = base_density.get(traffic_condition.lower(), base_density['normal'])
        
        # Lấy độ rộng và loại đường
        route_width, route_type = get_route_info(net, route_id, routes)
        
        # Điều chỉnh theo độ rộng (4m là chuẩn)
        scale_width = min(2.0, route_width / 4.0)  # Tăng tối đa 2x cho đường rộng
        # Điều chỉnh theo loại đường
        scale_type = 1.5 if "primary" in route_type else 0.5 if "residential" in route_type else 1.0
        # Tính tốc độ (km/h) từ duration_seconds
        speed = (distance_meters / max(duration_seconds, 1)) * 3.6  # m/s to km/h
        speed = max(5.0, min(speed, 40.0))  # Giới hạn tốc độ 5-40 km/h
        
        # Chuyển mật độ thành lưu lượng (xe/giờ = xe/km × km/h)
        counts = {k: int(v * scale_width * scale_type * speed) for k, v in density.items()}
        
        # Giới hạn lưu lượng tối đa (dựa trên Jakarta và Hà Nội)
        max_flow = {'motorcycle': 1000, 'car': 300, 'bus': 20, 'truck': 15}
        counts = {k: min(v, max_flow[k]) for k, v in counts.items()}
        
        return counts
    except Exception as e:
        print(f"[ERROR] Failed to estimate vehicle counts: {e}. Using default.")
        return {'motorcycle': 300, 'car': 50, 'bus': 5, 'truck': 3}

def find_closest_node(net, lat, lng):
    # nó tương tự như một hàm tìm giá trị bé nhất, gán cái đầu tiên nhỏ nhất rồi sau đó loop qua để tìm cái bé nhất
    """
    Tìm node gần nhất trong mạng SUMO dựa trên tọa độ lat, lng.
    
    Args:
        net: Mạng SUMO
        lat, lng: Tọa độ của giao lộ
    
    Returns:
        str: ID của node gần nhất hoặc None nếu không tìm thấy
    """
    try:
        min_dist = float('inf')
        closest_node = None
        for node in net.getNodes():
            x, y = node.getCoord()
            # Giả định tọa độ x, y trong SUMO gần với lat, lng
            # Tính khoảng cách Euclidean giữa tọa độ đầu vào (lat, lng) và tọa độ node (x, y)
            dist = ((lat - x) ** 2 + (lng - y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_node = node.getID()
        return closest_node
    except Exception as e:
        print(f"[ERROR] Failed to find closest node for lat={lat}, lng={lng}: {e}")
        return None

def find_route(net, from_node, to_node, vehicle_id, routes):
    """
    Tìm đường đi ngắn nhất giữa hai node và thêm route vào file .rou.xml.
    
    Args:
        net: Mạng SUMO
        from_node, to_node: ID của node nguồn và đích
        vehicle_id: ID để tạo route duy nhất
        routes: ElementTree root của file .rou.xml
    
    Returns:
        str: ID của route hoặc None nếu không tìm thấy
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
    Tạo các flow cho file .rou.xml dựa trên dữ liệu giao thông.
    
    Args:
        routes: ElementTree root
        net: Mạng SUMO
        traffic_data: DataFrame chứa dữ liệu giao thông
        intersection_mapping: Dict ánh xạ tên giao lộ sang node ID
        simulation_period: Thời gian mô phỏng (giây)
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
                    
                    # Ước tính lưu lượng dựa trên mật độ
                    counts = estimate_vehicle_counts(
                        row['traffic_condition'],
                        row['distance_meters'],
                        row['duration_seconds'],
                        route_id,
                        routes,
                        net
                    )
                    
                    # Tạo flow cho từng loại phương tiện 
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
    Tạo file .rou.xml từ dữ liệu lưu lượng giao thông.
    
    Args:
        net_file: Đường dẫn đến file .net.xml
        traffic_data_files: List các file CSV giao thông
        intersection_file: File CSV chứa tọa độ giao lộ
        output_file: Đường dẫn đến file .rou.xml
        simulation_period: Thời gian mô phỏng (giây, mặc định: 3 ngày)
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
        "data/traffic/traffic_data_Wednesday_2025-05-14.csv",
        "data/traffic/traffic_data_Thursday_2025-05-15.csv",
        "data/traffic/traffic_data_Friday_2025-05-16.csv"
    ]
    create_route_file(
        net_file="sumo_files/network/region_1.net.xml",
        traffic_data_files=traffic_data_files,
        intersection_file="data/intersection_list.csv",
        output_file="sumo_files/routes/region_1.rou.xml",
        simulation_period=259200
    )