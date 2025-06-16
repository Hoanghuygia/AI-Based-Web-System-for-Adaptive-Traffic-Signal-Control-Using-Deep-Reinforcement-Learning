import xml.etree.ElementTree as ET
import sumolib
import os

def fix_calibrators():
    print("=== SỬA CALIBRATOR POSITIONS ===\n")
    
    # Kiểm tra file tồn tại
    net_file = "network/region_1.net.xml"
    cal_file = "additional/calibrator.xml"
    
    if not os.path.exists(net_file):
        print(f"❌ Không tìm thấy file: {net_file}")
        return
    
    if not os.path.exists(cal_file):
        print(f"❌ Không tìm thấy file: {cal_file}")
        return
    
    try:
        # Đọc network
        print("Đang đọc network...")
        net = sumolib.net.readNet(net_file)
        print(f"✅ Network đã được đọc thành công")
        
        # Đọc calibrators
        print("Đang đọc calibrators...")
        tree = ET.parse(cal_file)
        root = tree.getroot()
        
        # Tìm các loại calibrator có thể có
        calibrators = []
        calibrators.extend(root.findall("calibrator"))
        calibrators.extend(root.findall("variableSpeedSign"))
        calibrators.extend(root.findall("rerouter"))
        
        print(f"✅ Tìm thấy {len(calibrators)} calibrator(s)\n")
        
        if len(calibrators) == 0:
            print("❌ Không có calibrator nào trong file!")
            # In ra nội dung file để kiểm tra
            with open(cal_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print("Nội dung file calibrator.xml (500 ký tự đầu):")
                print(content[:500] + "...")
            return
        
        problem_calibrators = []
        fixed_count = 0
        
        for i, cal in enumerate(calibrators):
            cal_id = cal.get("id")
            edge_id = cal.get("edge")
            pos_str = cal.get("pos")
            
            if i < 10:  # Chỉ in 10 calibrator đầu
                print(f"Calibrator {i+1}: {cal_id}")
                print(f"  Edge: {edge_id}")
                print(f"  Position: {pos_str}")
            elif i == 10:
                print("...")
            
            if not pos_str:
                if i < 10:
                    print(f"  ❌ Không có thuộc tính 'pos'")
                continue
                
            try:
                pos = float(pos_str)
            except ValueError:
                if i < 10:
                    print(f"  ❌ Position không hợp lệ: {pos_str}")
                continue
            
            try:
                # Kiểm tra edge tồn tại
                edge = net.getEdge(edge_id)
                edge_len = edge.getLength()
                
                if i < 10:
                    print(f"  Edge length: {edge_len}")
                
                if pos >= edge_len:
                    if i < 10:
                        print(f"  ❌ PROBLEM: Position {pos} >= Edge length {edge_len}")
                    
                    # Sửa position - đặt cách cuối edge 2 mét để an toàn
                    safe_pos = max(0, edge_len - 2.0)
                    cal.set("pos", str(safe_pos))
                    fixed_count += 1
                    
                    problem_calibrators.append({
                        'id': cal_id,
                        'edge': edge_id,
                        'old_pos': pos,
                        'new_pos': safe_pos,
                        'edge_len': edge_len
                    })
                else:
                    if i < 10:
                        print(f"  ✅ OK: Position {pos} < Edge length {edge_len}")
                        
            except Exception as e:
                if i < 10:
                    print(f"  ❌ Lỗi với edge {edge_id}: {str(e)}")
                # Nếu edge không tồn tại, có thể xóa calibrator này
                problem_calibrators.append({
                    'id': cal_id,
                    'edge': edge_id,
                    'error': str(e),
                    'remove': True
                })
            
            if i < 10:
                print()
        
        print(f"\n=== TỔNG KẾT ===")
        print(f"Tổng số calibrator: {len(calibrators)}")
        print(f"Calibrator đã sửa: {fixed_count}")
        
        if problem_calibrators:
            print(f"\nCác calibrator đã được xử lý:")
            for i, prob in enumerate(problem_calibrators[:15]):  # Hiển thị 15 đầu
                if 'error' in prob:
                    if prob.get('remove'):
                        print(f"  {i+1}. {prob['id']}: LỖI - {prob['error']} (sẽ bị xóa)")
                    else:
                        print(f"  {i+1}. {prob['id']}: LỖI - {prob['error']}")
                else:
                    print(f"  {i+1}. {prob['id']}: {prob['old_pos']:.1f} -> {prob['new_pos']:.1f} (edge: {prob['edge_len']:.1f})")
            
            if len(problem_calibrators) > 15:
                print(f"  ... và {len(problem_calibrators) - 15} calibrator khác")
            
            # Xóa các calibrator có lỗi edge không tồn tại
            removed_count = 0
            for prob in problem_calibrators:
                if prob.get('remove'):
                    # Tìm và xóa calibrator này
                    for cal in calibrators:
                        if cal.get("id") == prob['id']:
                            root.remove(cal)
                            removed_count += 1
                            break
            
            if removed_count > 0:
                print(f"\nĐã xóa {removed_count} calibrator có edge không tồn tại")
            
            # Lưu file đã sửa
            output_file = "additional/calibrator_fixed.xml"
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            print(f"\n✅ Đã lưu file đã sửa: {output_file}")
            
            # Cập nhật file cấu hình
            print("\n📝 Cập nhật file region_1.sumocfg:")
            print("Thay đổi dòng:")
            print("  <additional-files value=\"additional/detectors_fixed.xml,additional/calibrator.xml\"/>")
            print("Thành:")
            print("  <additional-files value=\"additional/detectors_fixed.xml,additional/calibrator_fixed.xml\"/>")
            
        else:
            print("✅ Tất cả calibrator đều OK!")
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_calibrators()