import xml.etree.ElementTree as ET

def extract_junctions(net_file_path):
    """
    Extract junction information from a SUMO .net.xml file
    
    Args:
        net_file_path (str): Path to the .net.xml file
        
    Returns:
        list: List of dictionaries containing junction information
    """
    # Parse the XML file
    tree = ET.parse(net_file_path)
    root = tree.getroot()
    
    junctions = []
    
    # Extract junction information
    for junction in root.findall('.//junction'):
        junction_id = junction.get('id')
        
        # Skip internal junctions if needed (those with ":"" in their ID)
        # if ":" in junction_id:
        #     continue
        
        x = float(junction.get('x', 0))
        y = float(junction.get('y', 0))
        junction_type = junction.get('type', '')
        
        # Additional attributes you might be interested in
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

def print_junctions(junctions):
    """Print junction information in a readable format"""
    print(f"Found {len(junctions)} junctions:")
    print("-" * 60)
    print(f"{'ID':<20} {'X':>10} {'Y':>10} {'Type':<15}")
    print("-" * 60)
    
    for junction in junctions:
        print(f"{junction['id']:<20} {junction['x']:>10.6f} {junction['y']:>10.6f} {junction['type']:<15}")

def main():
    # File path to your .net.xml file
    net_file_path = "src/model/sumo_files/network/region_1.net.xml"  # Change this to your file path
    
    try:
        # Extract junction information
        junctions = extract_junctions(net_file_path)
        
        # Print junction information
        print_junctions(junctions)
        
        # Optionally, save to CSV
        # import csv
        # with open('junctions.csv', 'w', newline='') as csvfile:
        #     fieldnames = ['id', 'x', 'y', 'type']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for junction in junctions:
        #         writer.writerow({k: junction[k] for k in fieldnames})
        
    except Exception as e:
        print(f"Error: {e}") 

if __name__ == "__main__":
    main()