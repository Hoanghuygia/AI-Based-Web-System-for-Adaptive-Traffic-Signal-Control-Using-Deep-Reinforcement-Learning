import xml.etree.ElementTree as ET

def count_vehicles_in_route_file(route_file):
    tree = ET.parse(route_file)
    root = tree.getroot()
    
    vehicle_count = 0
    flow_count = 0
    total_flow_vehicles = 0
    
    # Đếm xe riêng lẻ
    vehicles = root.findall('.//vehicle')
    vehicle_count = len(vehicles)
    
    # Đếm flow và tính tổng xe từ flow
    flows = root.findall('.//flow')
    for flow in flows:
        flow_count += 1
        # Lấy số lượng xe từ flow
        number = flow.get('number')
        if number:
            total_flow_vehicles += int(number)
    
    print(f"Xe riêng lẻ: {vehicle_count}")
    print(f"Số flow: {flow_count}")
    print(f"Xe từ flow: {total_flow_vehicles}")
    print(f"Tổng cộng: {vehicle_count + total_flow_vehicles}")

# Sử dụng
count_vehicles_in_route_file("region_1.rou.xml")