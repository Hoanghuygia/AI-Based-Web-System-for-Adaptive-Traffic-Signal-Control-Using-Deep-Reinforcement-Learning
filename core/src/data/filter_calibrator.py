import xml.etree.ElementTree as ET
import argparse

def is_demand_zero(demand_elem):
    """Check if the demand has 0 vehicles"""
    number = demand_elem.get('number')
    weight = demand_elem.get('weight')
    vehs_per_hour = demand_elem.get('vehsPerHour')

    if number is not None and float(number) == 0:
        return True
    if weight is not None and float(weight) == 0:
        return True
    if vehs_per_hour is not None and float(vehs_per_hour) == 0:
        return True

    return False

def simplify_calibrator(input_path: str, output_path: str):
    tree = ET.parse(input_path)
    root = tree.getroot()

    total = 0
    removed = 0

    for calibrator in list(root.findall('calibrator')):
        total += 1
        demands = calibrator.findall('demand')
        
        if all(is_demand_zero(d) for d in demands):
            root.remove(calibrator)
            removed += 1

    tree.write(output_path, encoding='UTF-8', xml_declaration=True)
    print(f"✅ Đã xử lý: {total} calibrators")
    print(f"🗑️  Đã loại bỏ: {removed} calibrators (không có dòng xe)")
    print(f"💾 File đã lưu vào: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Làm nhẹ file calibrator SUMO bằng cách lọc các calibrator không có dòng xe.")
    parser.add_argument("input", help="Đường dẫn đến file calibrator gốc (.xml)")
    parser.add_argument("output", help="Đường dẫn lưu file calibrator sau khi lọc")

    args = parser.parse_args()
    simplify_calibrator(args.input, args.output)
