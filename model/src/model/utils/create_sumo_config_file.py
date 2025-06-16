import xml.etree.ElementTree as ET
import os

def create_sumo_config(net_file, route_file, traffic_light_file, output_file, begin_time=0, end_time=3600):
    """
    Tạo file cấu hình SUMO (.sumocfg)
    """
    # Tạo root element
    configuration = ET.Element("configuration")
    
    # Cấu hình input
    input_section = ET.SubElement(configuration, "input")
    
    # Thêm file mạng lưới đường
    net_file_elem = ET.SubElement(input_section, "net-file")
    net_file_elem.set("value", os.path.basename(net_file))
    
    # Thêm file route
    route_file_elem = ET.SubElement(input_section, "route-files")
    route_file_elem.set("value", os.path.basename(route_file))
    
    # Thêm file đèn tín hiệu
    add_file_elem = ET.SubElement(input_section, "additional-files")
    add_file_elem.set("value", os.path.basename(traffic_light_file))
    
    # Cấu hình thời gian
    time_section = ET.SubElement(configuration, "time")
    
    # Thời gian bắt đầu mô phỏng
    begin_elem = ET.SubElement(time_section, "begin")
    begin_elem.set("value", str(begin_time))
    
    # Thời gian kết thúc mô phỏng
    end_elem = ET.SubElement(time_section, "end")
    end_elem.set("value", str(end_time))
    
    # Cấu hình output
    output_section = ET.SubElement(configuration, "output")
    
    # File tripinfo
    tripinfo_elem = ET.SubElement(output_section, "tripinfo-output")
    tripinfo_elem.set("value", "tripinfo.xml")
    
    # File summary
    summary_elem = ET.SubElement(output_section, "summary-output")
    summary_elem.set("value", "summary.xml")
    
    # File queue
    queue_elem = ET.SubElement(output_section, "queue-output")
    queue_elem.set("value", "queue.xml")
    
    # Cấu hình tracing
    traci_section = ET.SubElement(configuration, "traci_server")
    remote_port_elem = ET.SubElement(traci_section, "remote-port")
    remote_port_elem.set("value", "8813")
    
    # Các cấu hình khác
    report_section = ET.SubElement(configuration, "report")
    
    # Tắt hiển thị GUI mặc định
    no_warnings_elem = ET.SubElement(report_section, "no-warnings")
    no_warnings_elem.set("value", "true")
    
    verbose_elem = ET.SubElement(report_section, "verbose")
    verbose_elem.set("value", "true")
    
    # Tạo cây XML
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    tree = ET.ElementTree(configuration)
    
    # Lưu file .sumocfg
    ET.indent(tree.getroot(), space="  ")  
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"SUMO configuration file created: {output_file}")

# Tạo file cấu hình SUMO
# create_sumo_config(
#     net_file='sumo_files/network/tan_binh.net.xml',
#     route_file='sumo_files/routes/tan_binh.rou.xml',
#     traffic_light_file='sumo_files/traffic_lights/tan_binh_tls.add.xml',
#     output_file='sumo_files/tan_binh.sumocfg',
#     begin_time=0,
#     end_time=3600
# )