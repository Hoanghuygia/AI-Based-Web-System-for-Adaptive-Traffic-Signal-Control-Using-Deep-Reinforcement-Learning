import xml.etree.ElementTree as ET
import os

def create_sumocfg(net_file, route_file, output_file="generated.sumocfg",
                   additional_files=None, begin_time=0, end_time=1000):
    """
    Tạo file SUMO configuration (.sumocfg)
    
    Args:
        net_file: Đường dẫn đến file .net.xml
        route_file: Đường dẫn đến file .rou.xml
        output_file: Tên file output (mặc định: generated.sumocfg)
        additional_files: List các file additional (detector, calibrator,...)
        begin_time: Thời gian bắt đầu mô phỏng (mặc định: 0)
        end_time: Thời gian kết thúc mô phỏng (mặc định: 1000)
    """
    
    # Validation - kiểm tra file input có tồn tại không
    if not os.path.exists(net_file):
        print(f"Warning: {net_file} không tồn tại")
    if not os.path.exists(route_file):
        print(f"Warning: {route_file} không tồn tại")
    
    # Tạo root element
    config = ET.Element("configuration")
    
    # Input section
    input_elem = ET.SubElement(config, "input")
    ET.SubElement(input_elem, "net-file", value=net_file)
    ET.SubElement(input_elem, "route-files", value=route_file)
    
    # Thêm additional files nếu có
    if additional_files:
        # Kiểm tra các file additional có tồn tại không
        existing_files = []
        for f in additional_files:
            if os.path.exists(f):
                existing_files.append(f)
            else:
                print(f"Warning: {f} không tồn tại")
        
        if existing_files:
            ET.SubElement(input_elem, "additional-files", value=",".join(existing_files))
    
    # Time section
    time_elem = ET.SubElement(config, "time")
    ET.SubElement(time_elem, "begin", value=str(begin_time))
    ET.SubElement(time_elem, "end", value=str(end_time))
    
    # Processing section - thêm một số cấu hình hữu ích
    processing_elem = ET.SubElement(config, "processing")
    ET.SubElement(processing_elem, "ignore-route-errors", value="true")
    
    # Report section
    report_elem = ET.SubElement(config, "report")
    ET.SubElement(report_elem, "verbose", value="true")
    ET.SubElement(report_elem, "no-step-log", value="true")
    
    # Format XML đẹp hơn với indentation
    def prettify_xml(element, level=0):
        """Làm đẹp XML với proper indentation"""
        indent = "\n" + "    " * level  # 4 spaces per level
        
        if len(element):
            if not element.text or not element.text.strip():
                element.text = indent + "    "
            if not element.tail or not element.tail.strip():
                element.tail = indent
            for child in element:
                prettify_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not element.tail or not element.tail.strip()):
                element.tail = indent
    
    # Áp dụng formatting
    prettify_xml(config)
    
    # Ghi file với pretty format
    tree = ET.ElementTree(config)
    
    # Tạo XML string với format đẹp
    rough_string = ET.tostring(config, encoding='unicode')
    
    # Ghi file với XML declaration và format đẹp
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(rough_string)
    print(f"✅ Generated {output_file} successfully!")

if __name__ == "__main__":
    # Ví dụ sử dụng - sử dụng tên file thực tế
    create_sumocfg(
        net_file="region_1.net.xml",
        route_file="generated_routes.rou.xml",  # Sửa tên file này
        output_file="traffic_simulation.sumocfg",
        additional_files=["calibrator_fixed.xml", "detectors_fixed.xml"],  # Sửa tên file này
        begin_time=0,
        end_time=3600  # 1 giờ mô phỏng
    )
    
    print("\n📋 File configuration đã được tạo với nội dung:")
    print("- Network file: region_1.net.xml")
    print("- Route file: generated_rou.rou.xml")
    print("- Additional files: calibrator_fixed.xml, detector_fixed.xml")
    print("- Simulation time: 0-3600 seconds")