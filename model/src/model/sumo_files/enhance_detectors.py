import xml.etree.ElementTree as ET
import sumolib
import os

def fix_induction_loops():
    print("=== SỬA INDUCTION LOOP DETECTORS ===\n")
    
    # Kiểm tra file tồn tại
    net_file = "network/region_1.net.xml"
    det_file = "additional/detectors_new.xml"
    
    if not os.path.exists(net_file):
        print(f"❌ Không tìm thấy file: {net_file}")
        return
    
    if not os.path.exists(det_file):
        print(f"❌ Không tìm thấy file: {det_file}")
        return
    
    try:
        # Đọc network
        print("Đang đọc network...")
        net = sumolib.net.readNet(net_file)
        print(f"✅ Network đã được đọc thành công")
        
        # Đọc detectors
        print("Đang đọc detectors...")
        tree = ET.parse(det_file)
        root = tree.getroot()
        
        # Tìm inductionLoop thay vì e1Detector
        detectors = root.findall("inductionLoop")
        print(f"✅ Tìm thấy {len(detectors)} inductionLoop detector(s)\n")
        
        if len(detectors) == 0:
            print("❌ Không có inductionLoop nào trong file!")
            return
        
        problem_detectors = []
        fixed_count = 0
        
        for i, det in enumerate(detectors):
            det_id = det.get("id")
            lane_id = det.get("lane")
            pos_str = det.get("pos")
            
            if i < 10:  # Chỉ in 10 detector đầu để tránh spam
                print(f"Detector {i+1}: {det_id}")
                print(f"  Lane: {lane_id}")
                print(f"  Position: {pos_str}")
            elif i == 10:
                print("...")
            
            if not pos_str:
                print(f"  ❌ Không có thuộc tính 'pos'")
                continue
                
            try:
                pos = float(pos_str)
            except ValueError:
                print(f"  ❌ Position không hợp lệ: {pos_str}")
                continue
            
            try:
                # Kiểm tra lane tồn tại
                lane = net.getLane(lane_id)
                lane_len = lane.getLength()
                
                if i < 10:
                    print(f"  Lane length: {lane_len}")
                
                if pos >= lane_len:
                    if i < 10:
                        print(f"  ❌ PROBLEM: Position {pos} >= Lane length {lane_len}")
                    
                    # Sửa position
                    safe_pos = max(0, lane_len - 1.0)
                    det.set("pos", str(safe_pos))
                    fixed_count += 1
                    
                    problem_detectors.append({
                        'id': det_id,
                        'lane': lane_id,
                        'old_pos': pos,
                        'new_pos': safe_pos,
                        'lane_len': lane_len
                    })
                else:
                    if i < 10:
                        print(f"  ✅ OK: Position {pos} < Lane length {lane_len}")
                        
            except Exception as e:
                if i < 10:
                    print(f"  ❌ Lỗi với lane {lane_id}: {str(e)}")
                problem_detectors.append({
                    'id': det_id,
                    'lane': lane_id,
                    'error': str(e)
                })
            
            if i < 10:
                print()
        
        print(f"\n=== TỔNG KẾT ===")
        print(f"Tổng số detector: {len(detectors)}")
        print(f"Detector đã sửa: {fixed_count}")
        
        if problem_detectors:
            print(f"\nCác detector đã được sửa:")
            for i, prob in enumerate(problem_detectors[:10]):  # Chỉ hiển thị 10 đầu
                if 'error' in prob:
                    print(f"  {i+1}. {prob['id']}: LỖI - {prob['error']}")
                else:
                    print(f"  {i+1}. {prob['id']}: {prob['old_pos']} -> {prob['new_pos']} (lane: {prob['lane_len']})")
            
            if len(problem_detectors) > 10:
                print(f"  ... và {len(problem_detectors) - 10} detector khác")
            
            # Lưu file đã sửa
            output_file = "additional/detectors_fixed.xml"
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            print(f"\n✅ Đã lưu file đã sửa: {output_file}")
            
            # Cập nhật file cấu hình
            print("\n📝 Cập nhật file region_1.sumocfg:")
            print("Thay đổi dòng:")
            print("  <additional-files value=\"additional/detectors.xml,additional/calibrator.xml\"/>")
            print("Thành:")
            print("  <additional-files value=\"additional/detectors_fixed.xml,additional/calibrator.xml\"/>")
            
        else:
            print("✅ Tất cả detector đều OK!")
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_induction_loops()