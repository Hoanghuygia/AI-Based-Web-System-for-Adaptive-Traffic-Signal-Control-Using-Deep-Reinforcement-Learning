import xml.etree.ElementTree as ET
from collections import defaultdict
import argparse

def optimize_calibrator(input_file: str, output_file: str):
    tree = ET.parse(input_file)
    root = tree.getroot()

    edge_hour_map = defaultdict(lambda: {"vehsPerHour": 0, "speed_total": 0, "count": 0})

    for cal in root.findall("calibrator"):
        edge = cal.get("edge")
        pos = cal.get("pos", "10")  # giữ vị trí
        period = cal.get("period", "300")

        flow = cal.find("flow")
        if flow is None:
            continue

        begin = int(flow.get("begin"))
        end = int(flow.get("end"))
        hour = begin // 3600  # group theo giờ

        vehs_per_hour = int(flow.get("vehsPerHour", 0))
        speed = float(flow.get("speed", 10))

        key = (edge, hour, pos, period)

        edge_hour_map[key]["vehsPerHour"] += vehs_per_hour
        edge_hour_map[key]["speed_total"] += speed
        edge_hour_map[key]["count"] += 1

    # Ghi ra file mới
    new_root = ET.Element("additional")
    for (edge, hour, pos, period), data in edge_hour_map.items():
        begin = hour * 3600
        end = begin + 3600
        avg_speed = data["speed_total"] / data["count"]

        cal = ET.SubElement(new_root, "calibrator", attrib={
            "id": f"opt_cal_{edge}_{begin}_{end}",
            "edge": edge,
            "pos": pos,
            "period": period
        })
        ET.SubElement(cal, "flow", attrib={
            "begin": str(begin),
            "end": str(end),
            "vehsPerHour": str(int(data["vehsPerHour"])),
            "speed": str(round(avg_speed, 2))
        })

    tree = ET.ElementTree(new_root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"[INFO] Optimized calibrator saved to {output_file}")

# ===================
# Chạy script trực tiếp
# ===================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize a SUMO calibrator file to reduce size.")
    parser.add_argument("input", help="Path to the original calibrator XML file")
    parser.add_argument("output", help="Path to the optimized calibrator XML file")
    args = parser.parse_args()

    optimize_calibrator(args.input, args.output)
