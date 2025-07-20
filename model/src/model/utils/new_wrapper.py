import subprocess
import xml.etree.ElementTree as ET
import pandas as pd
import os
import tempfile
import sumolib
import glob
import random
import numpy as np

class SUMORandomTripsWrapper:
    def __init__(self, net_file, traffic_data_files, routes_file=None):
        self.net_file = net_file
        self.routes_file = routes_file
        if isinstance(traffic_data_files, str) and os.path.isdir(traffic_data_files):
            self.traffic_data_files = glob.glob(os.path.join(traffic_data_files, "*.csv"))
            if not self.traffic_data_files:
                raise ValueError(f"No CSV files found in directory {traffic_data_files}")
        else:
            self.traffic_data_files = traffic_data_files if isinstance(traffic_data_files, list) else [traffic_data_files]
        print(f"Traffic data files: {self.traffic_data_files}")
        self.base_params = {
            'normal': {'period': 8, 'fringe_factor': 1, 'via_prob': 0.1},
            'moderate': {'period': 4, 'fringe_factor': 3, 'via_prob': 0.25},
            'heavy': {'period': 2, 'fringe_factor': 5, 'via_prob': 0.4}
        }
        self.vehicle_types = [
            {"id": "motorcycle", "vClass": "motorcycle", "accel": "3.0", "decel": "5.0", "sigma": "0.7", "length": "2.0", "width": "0.8", "maxSpeed": "16.67", "color": "yellow", "minGap": "0.5", "lcAssertive": "1.6", "lcSpeedGain": "1.6", "lcStrategic": "1.3", "lcCooperative": "0.7"},
            {"id": "car", "vClass": "passenger", "accel": "2.5", "decel": "4.5", "sigma": "0.3", "length": "4.5", "width": "1.8", "maxSpeed": "13.89", "color": "blue", "minGap": "2.0", "lcAssertive": "1.2", "lcSpeedGain": "1.3", "lcStrategic": "1.6", "lcCooperative": "0.8"},
            {"id": "bus", "vClass": "bus", "accel": "1.5", "decel": "3.5", "sigma": "0.2", "length": "12.0", "width": "2.5", "maxSpeed": "11.11", "color": "green", "minGap": "3.0", "lcAssertive": "1.0", "lcSpeedGain": "1.0", "lcStrategic": "1.0", "lcCooperative": "1.0"},
            {"id": "truck", "vClass": "truck", "accel": "1.8", "decel": "4.0", "sigma": "0.2", "length": "7.5", "width": "2.2", "maxSpeed": "11.11", "color": "red", "minGap": "3.0", "lcAssertive": "1.0", "lcSpeedGain": "1.0", "lcStrategic": "1.0", "lcCooperative": "1.0"}
        ]

    def load_traffic_data(self):
        required_columns = ['hour_of_day', 'traffic_condition', 'duration_seconds', 'distance_meters']
        if not self.traffic_data_files:
            raise ValueError("No traffic data files provided")
        data = pd.concat([pd.read_csv(f) for f in self.traffic_data_files], ignore_index=True)
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"CSV file must contain columns: {required_columns}")
        return data

    def analyze_traffic_patterns(self, traffic_data):
        patterns = {}
        for hour in traffic_data['hour_of_day'].unique():
            hour_data = traffic_data[traffic_data['hour_of_day'] == hour]
            condition = hour_data['traffic_condition'].mode().iloc[0]
            avg_duration = hour_data['duration_seconds'].mean()
            avg_distance = hour_data['distance_meters'].mean()
            patterns[hour] = {'condition': condition, 'avg_duration': avg_duration, 'avg_distance': avg_distance}
        return patterns

    def create_vehicle_types_file(self):
        """Create a file with all vehicle type definitions"""
        root = ET.Element('additional')
        for vtype in self.vehicle_types:
            ET.SubElement(root, 'vType', attrib=vtype)
        
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w")
        temp_name = temp.name
        print(f"[DEBUG] Creating vtypes file: {temp_name}")
        ET.ElementTree(root).write(temp_name, encoding="utf-8", xml_declaration=True)
        temp.close()
        return temp_name

    def get_route_info(self, net, route_id, routes):
        try:
            route = routes.find(f".//route[@id='{route_id}']")
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
            print(f"[WARNING] Failed to get route info for {route_id}: {e}. Using defaults.")
            return 4.0, "highway.secondary"

    def estimate_vehicle_counts(self, traffic_condition, distance_meters, duration_seconds, route_id, routes, net):
        try:
            base_density = {
                'normal': {'motorcycle': 2000, 'car': 200, 'bus': 20, 'truck': 10},
                'moderate': {'motorcycle': 4000, 'car': 300, 'bus': 40, 'truck': 20},
                'heavy': {'motorcycle': 6000, 'car': 400, 'bus': 60, 'truck': 30}
            }
            density = base_density.get(traffic_condition.lower(), base_density['normal'])
            
            if route_id and routes and net:
                route_width, route_type = self.get_route_info(net, route_id, routes)
            else:
                route_width, route_type = 4.0, "highway.secondary"
            
            scale_width = min(2.0, route_width / 4.0)
            scale_type = 1.5 if "primary" in route_type else 0.5 if "residential" in route_type else 1.0
            speed = (distance_meters / max(duration_seconds, 1)) * 3.6
            speed = max(5.0, min(speed, 40.0))
            
            counts = {k: int(v * scale_width * scale_type * speed) for k, v in density.items()}
            max_flow = {'motorcycle': 10000, 'car': 3000, 'bus': 200, 'truck': 150}
            counts = {k: min(v, max_flow[k]) for k, v in counts.items()}
            
            return counts, speed
        except Exception as e:
            print(f"[ERROR] Failed to estimate vehicle counts: {e}. Using default.")
            return {'motorcycle': 300, 'car': 50, 'bus': 5, 'truck': 3}, 10.0

    def assign_vehicle_types(self, vehicles, hour_pattern):
        """Assign vehicle types to vehicles based on traffic pattern"""
        counts, _ = self.estimate_vehicle_counts(
            hour_pattern['condition'], 
            hour_pattern['avg_distance'], 
            hour_pattern['avg_duration'], 
            None, None, None
        )
        
        # Calculate probabilities
        total = sum(counts.values())
        if total == 0:
            probabilities = [0.25, 0.25, 0.25, 0.25]  # Equal distribution
        else:
            probabilities = [
                counts['motorcycle'] / total,
                counts['car'] / total, 
                counts['bus'] / total,
                counts['truck'] / total
            ]
        
        vehicle_type_names = ['motorcycle', 'car', 'bus', 'truck']
        
        print(f"[INFO] Vehicle type probabilities: {dict(zip(vehicle_type_names, probabilities))}")
        
        # Assign types to vehicles
        assigned_vehicles = []
        for vehicle in vehicles:
            # Choose vehicle type based on probabilities
            chosen_type = np.random.choice(vehicle_type_names, p=probabilities)
            
            # Set the type attribute
            vehicle.set('type', chosen_type)
            assigned_vehicles.append(vehicle)
            
        return assigned_vehicles

    def create_calibrator_file(self, patterns, output_file):
        root = ET.Element("additional")
        net = sumolib.net.readNet(self.net_file)
        routes = ET.parse(self.routes_file).getroot() if self.routes_file else None
        if not routes:
            print(f"[WARNING] No routes file loaded, calibrator.xml will be empty")
            ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)
            return
        
        route_counter = 0
        for hour, pattern in patterns.items():
            begin, end = hour * 3600, (hour + 1) * 3600
            for route in routes.findall(".//route"):
                route_id = route.get("id", f"route_{route_counter}")
                edges = route.get("edges", "").split()
                if not edges:
                    print(f"[WARNING] Route {route_id} has no edges, skipping")
                    continue
                counts, speed = self.estimate_vehicle_counts(
                    pattern['condition'], pattern['avg_distance'], pattern['avg_duration'], 
                    route_id, routes, net
                )
                total_vehs = sum(counts.values()) * 3600 / max(pattern['avg_duration'], 1)
                for edge_id in edges:
                    calibrator = ET.SubElement(root, "calibrator", attrib={
                        "id": f"cal_{edge_id}_{route_id}_{hour}",
                        "edge": edge_id,
                        "pos": "10",
                        "period": "300"
                    })
                    ET.SubElement(calibrator, "flow", attrib={
                        "begin": str(begin),
                        "end": str(end),
                        "vehsPerHour": str(int(total_vehs)),
                        "speed": str(speed)
                    })
                route_counter += 1
        
        if route_counter == 0:
            print(f"[WARNING] No valid routes found in {self.routes_file}")
        ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"[INFO] Saved calibrator file with {route_counter} routes to {output_file}")

    def create_detectors_file(self, output_file):
        root = ET.Element("additional")
        net = sumolib.net.readNet(self.net_file)
        for edge in net.getEdges():
            lanes = edge.getLanes()
            if lanes:
                ET.SubElement(root, "inductionLoop", attrib={
                    "id": f"det_{edge.getID()}",
                    "lane": f"{edge.getID()}_{lanes[0].getIndex()}",
                    "pos": "10",
                    "file": "detector_output.xml",
                    "period": "300"
                })
        ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"[INFO] Saved detectors file to {output_file}")

    def generate_routes_by_hour(self, patterns, output_file):
        all_routes = []
        all_vehicles_by_hour = {}  # Store vehicles by hour for type assignment
        
        sumo_home = os.environ.get("SUMO_HOME", "")
        if not sumo_home:
            raise ValueError("SUMO_HOME environment variable not set")
        random_trips = os.path.join(sumo_home, "tools", "randomTrips.py")
        
        try:
            for hour, pattern in patterns.items():
                print(f"[INFO] Generating hour {hour}: {pattern['condition']}")
                
                # Create temporary additional file with vehicle types
                vtypes_file = self.create_vehicle_types_file()
                begin, end = hour * 3600, (hour + 1) * 3600
                temp_route = f"temp_hour_{hour}.rou.xml"
                
                # Generate routes using randomTrips.py - WITHOUT specifying vtype
                cmd = [
                    "python", random_trips,
                    "-n", self.net_file, 
                    "-r", temp_route,
                    "--additional-file", vtypes_file,
                    # Remove the problematic --vtype parameter
                    "--period", str(self.base_params[pattern['condition'].lower()]['period']),
                    "--fringe-factor", str(self.base_params[pattern['condition'].lower()]['fringe_factor']),
                    "--begin", str(begin), 
                    "--end", str(end), 
                    "--validate"
                ]
                
                print(f"[DEBUG] Command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"[ERROR] randomTrips.py failed for hour {hour}: {result.stderr}")
                    continue
                
                if os.path.exists(temp_route):
                    # Parse the generated route file
                    root = ET.parse(temp_route).getroot()
                    hour_vehicles = []
                    
                    # Extract vehicles and routes
                    for elem in root:
                        if elem.tag == "vehicle":
                            hour_vehicles.append(elem)
                        elif elem.tag in ["trip", "flow", "route"]:
                            all_routes.append(elem)
                    
                    # Store vehicles by hour for type assignment
                    all_vehicles_by_hour[hour] = {
                        'vehicles': hour_vehicles,
                        'pattern': pattern
                    }
                    
                    os.remove(temp_route)
                
                # Clean up temporary files
                if os.path.exists(vtypes_file):
                    print(f"[DEBUG] Removing vtypes file: {vtypes_file}")
                    os.remove(vtypes_file)
                if os.path.exists("trips.trips.xml"):
                    print(f"[DEBUG] Removing unexpected file: trips.trips.xml")
                    os.remove("trips.trips.xml")
        
        finally:
            # Assign vehicle types and combine all routes
            self.combine_routes_with_types(all_vehicles_by_hour, all_routes, output_file)

    def combine_routes_with_types(self, vehicles_by_hour, other_routes, output_file):
        """Combine routes and assign vehicle types based on hour patterns"""
        root = ET.Element("routes")
        
        # Add vehicle type definitions
        for vtype in self.vehicle_types:
            ET.SubElement(root, 'vType', attrib=vtype)
        
        # Add other route elements (route definitions, etc.)
        for route in other_routes:
            root.append(route)
        
        # Process vehicles by hour and assign types
        total_vehicles = 0
        type_counts = {'motorcycle': 0, 'car': 0, 'bus': 0, 'truck': 0}
        
        for hour, hour_data in vehicles_by_hour.items():
            vehicles = hour_data['vehicles']
            pattern = hour_data['pattern']
            
            print(f"[INFO] Assigning types for hour {hour}: {len(vehicles)} vehicles")
            
            # Assign vehicle types based on traffic pattern
            assigned_vehicles = self.assign_vehicle_types(vehicles, pattern)
            
            # Add assigned vehicles to root
            for vehicle in assigned_vehicles:
                root.append(vehicle)
                vehicle_type = vehicle.get('type', 'car')
                type_counts[vehicle_type] += 1
                total_vehicles += 1
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write the final route file
        ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)
        
        print(f"[INFO] Saved {total_vehicles} vehicles to {output_file}")
        print(f"[INFO] Vehicle type distribution: {type_counts}")
        
        # Calculate and display percentages
        if total_vehicles > 0:
            percentages = {k: f"{(v/total_vehicles)*100:.1f}%" for k, v in type_counts.items()}
            print(f"[INFO] Vehicle type percentages: {percentages}")

    def generate(self, output_file):
        os.makedirs("../sumo_files/additional", exist_ok=True)
        traffic_data = self.load_traffic_data()
        patterns = self.analyze_traffic_patterns(traffic_data)
        
        # Generate routes with proper vehicle type assignment
        self.generate_routes_by_hour(patterns, output_file)
        self.routes_file = output_file
        
        # Generate additional files
        self.create_calibrator_file(patterns, "../sumo_files/additional/calibrator_new.xml")
        self.create_detectors_file("../sumo_files/additional/detectors_new.xml")

if __name__ == "__main__":
    wrapper = SUMORandomTripsWrapper(
        net_file="../sumo_files/network/region_1.net.xml",
        traffic_data_files="../data/traffic"
    )
    wrapper.generate("../sumo_files/routes/new_routes.rou.xml")