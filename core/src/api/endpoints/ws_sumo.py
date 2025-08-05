# src/api/endpoints/ws_sumo.py
# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# import traci
# import asyncio
# import json
# import base64
# from io import BytesIO
# import pyautogui

# router = APIRouter()

# @router.websocket("/ws/sumo")
# async def websocket_sumo_data(websocket: WebSocket):
#     await websocket.accept()
#     print("📡 WebSocket client connected")

#     selected_junction = None  # mặc định chưa có junction nào được chọn

#     try:
#         while True:
#             # Nhận dữ liệu từ frontend nếu có (VD: yêu cầu gửi thông tin junction cụ thể)
#             try:
#                 message = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
#                 data = json.loads(message)
#                 if "junction_id" in data:
#                     selected_junction = data["junction_id"]
#                     print(f"🔄 Selected junction: {selected_junction}")
#             except asyncio.TimeoutError:
#                 pass  # Không có gì được gửi từ frontend

#             # Gửi dữ liệu phương tiện
#             vehicles = traci.vehicle.getIDList()
#             vehicle_data = []

#             for veh_id in vehicles:
#                 pos = traci.vehicle.getPosition(veh_id)
#                 speed = traci.vehicle.getSpeed(veh_id)
#                 vehicle_data.append({
#                     "id": veh_id,
#                     "position": pos,
#                     "speed": speed
#                 })

#             # Gửi dữ liệu traffic light nếu junction đã được chọn
#             traffic_light_info = {}
#             if selected_junction:
#                 try:
#                     phase = traci.trafficlight.getPhase(selected_junction)
#                     traffic_light_info = {
#                         "id": selected_junction,
#                         "phase": phase
#                     }
#                 except Exception as e:
#                     traffic_light_info = {
#                         "id": selected_junction,
#                         "error": f"Junction not found: {e}"
#                     }

#             await websocket.send_text(json.dumps({
#                 "vehicles": vehicle_data,
#                 "traffic_light": traffic_light_info
#             }))

#             await asyncio.sleep(1)

#     except WebSocketDisconnect:
#         print("🔌 WebSocket client disconnected")

# @router.websocket("/ws/sumo")
# async def websocket_sumo_data(websocket: WebSocket):
#     await websocket.accept()
#     print("📡 WebSocket client connected")

#     selected_junction = None  # mặc định chưa có junction nào được chọn

#     try:
#         while True:
#             # Nhận dữ liệu từ frontend nếu có
#             try:
#                 message = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
#                 data = json.loads(message)
#                 if "junction_id" in data:
#                     selected_junction = data["junction_id"]
#                     print(f"🔄 Selected junction: {selected_junction}")
#             except asyncio.TimeoutError:
#                 pass  # Không có gì được gửi từ frontend

#             # Gửi dữ liệu phương tiện
#             vehicles = traci.vehicle.getIDList()
#             vehicle_data = []
#             total_speed = 0.0

#             for veh_id in vehicles:
#                 pos = traci.vehicle.getPosition(veh_id)
#                 speed = traci.vehicle.getSpeed(veh_id)
#                 total_speed += speed
#                 vehicle_data.append({
#                     "id": veh_id,
#                     "position": pos,
#                     "speed": speed
#                 })

#             # Tính tốc độ trung bình
#             avg_speed = total_speed / len(vehicles) if vehicles else 0.0

#             # Xác định trạng thái giao thông
#             if avg_speed < 5:
#                 traffic_status = "heavy traffic"
#             elif avg_speed < 15:
#                 traffic_status = "moderate traffic"
#             else:
#                 traffic_status = "light traffic"

#             # Gửi dữ liệu traffic light nếu junction đã được chọn
#             traffic_light_info = {}
#             if selected_junction:
#                 try:
#                     phase = traci.trafficlight.getPhase(selected_junction)
#                     traffic_light_info = {
#                         "id": selected_junction,
#                         "phase": phase
#                     }
#                 except Exception as e:
#                     traffic_light_info = {
#                         "id": selected_junction,
#                         "error": f"Junction not found: {e}"
#                     }

#             # Gửi tất cả thông tin về frontend
#             await websocket.send_text(json.dumps({
#                 "vehicles": vehicle_data,
#                 "average_speed": avg_speed,
#                 "traffic_status": traffic_status,
#                 "traffic_light": traffic_light_info
#             }))

#             await asyncio.sleep(1)

#     except WebSocketDisconnect:
#         print("🔌 WebSocket client disconnected")

# @router.websocket("/ws/sumo-image")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             screenshot = pyautogui.screenshot()  # Capture toàn màn hình
#             # x, y, w, h = 706, 466, 200, 200
#             # Nếu bạn chỉ muốn phần SUMO-GUI: 
#             # screenshot = pyautogui.screenshot(region=(860, 650, 100, 65))

#             buffer = BytesIO()
#             screenshot.save(buffer, format="JPEG")
#             img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

#             await websocket.send_text(img_str)
#             await asyncio.sleep(1)  # Gửi mỗi 1 giây
#     except Exception as e:
#         print(f"WebSocket error: {e}")
#         await websocket.close()

# @router.websocket("/ws/sumo")
# async def websocket_sumo_data(websocket: WebSocket):
#     await websocket.accept()
#     print("📡 WebSocket client connected")

#     selected_junction = None  # mặc định chưa có junction nào được chọn

#     try:
#         while True:
#             try:
#                 message = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
#                 data = json.loads(message)
#                 print(f"Received data: {data}")
#                 if "junction_id" in data:
#                     selected_junction = data["junction_id"]
#                     print(f"🔄 Selected junction: {selected_junction}")
#             except asyncio.TimeoutError:
#                 pass

#             vehicle_data = []
#             avg_speed = 0.0
#             traffic_status = "N/A"  # Default

#             if selected_junction:
#                 try:
#                     # Thông tin traffic light
#                     phase = traci.trafficlight.getPhase(selected_junction)
#                     traffic_light_info = {
#                         "id": selected_junction,
#                         "phase": phase
#                     }

#                     # Các làn được điều khiển bởi junction này
#                     controlled_lanes = traci.trafficlight.getControlledLanes(selected_junction)
#                     total_speed = 0.0
#                     vehicle_count = 0

#                     for lane_id in controlled_lanes:
#                         veh_ids = traci.lane.getLastStepVehicleIDs(lane_id)
#                         for veh_id in veh_ids:
#                             speed = traci.vehicle.getSpeed(veh_id)
#                             pos = traci.vehicle.getPosition(veh_id)

#                             total_speed += speed
#                             vehicle_count += 1

#                             vehicle_data.append({
#                                 "id": veh_id,
#                                 "position": pos,
#                                 "speed": speed
#                             })

#                     # Tính tốc độ trung bình
#                     avg_speed = total_speed / vehicle_count if vehicle_count > 0 else 0.0

#                     # Phân loại giao thông
#                     if avg_speed < 5:
#                         traffic_status = "heavy traffic"
#                     elif avg_speed < 15:
#                         traffic_status = "moderate traffic"
#                     else:
#                         traffic_status = "light traffic"

#                 except Exception as e:
#                     traffic_light_info = {
#                         "id": selected_junction,
#                         "error": f"Junction not found: {e}"
#                     }
#             else:
#                 traffic_light_info = {}

#             # Gửi dữ liệu về frontend
#             await websocket.send_text(json.dumps({
#                 "vehicles": vehicle_data,
#                 "average_speed": avg_speed,
#                 "traffic_status": traffic_status,
#                 "traffic_light": traffic_light_info
#             }))

#             await asyncio.sleep(1)

#     except WebSocketDisconnect:
#         print("🔌 WebSocket client disconnected")

# VIEW_ID = "View #0"

# @router.websocket("/ws/sumo-image")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             #* Kiểm tra có message từ FE không*
#             if websocket.client_state.name == "CONNECTED":
#                 try:
#                     message = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
#                     data = json.loads(message)  # Parse JSON
#                     print(f"Received data: {data}")
                    
#                     if "junction_id" in data:
#                         junction_id = data["junction_id"]
#                         print(f"Junction: {junction_id}")
                        
#                         #* Lấy tọa độ junction*
#                         pos = traci.junction.getPosition(junction_id)
#                         #* Di chuyển camera tới junction*
#                         traci.gui.setOffset(VIEW_ID, pos[0], pos[1])
#                         #* Zoom mức phù hợp (tuỳ bạn điều chỉnh)*
#                         traci.gui.setZoom(VIEW_ID, 50)
                        
#                 except asyncio.TimeoutError:
#                     #* Không có message mới thì bỏ qua*
#                     pass
#                 except json.JSONDecodeError as e:
#                     print(f"JSON decode error: {e}")
#                     pass
                    
#             #* Chụp màn hình toàn GUI*
#             screenshot = pyautogui.screenshot()
#             #* Convert sang base64*
#             buffer = BytesIO()
#             screenshot.save(buffer, format="JPEG")
#             img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
#             #* Gửi về FE*
#             await websocket.send_text(img_str)
#             await asyncio.sleep(1)
            
#     except Exception as e:
#         print(f"WebSocket error: {e}")
#         await websocket.close()


from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import pyautogui
import traci
import asyncio, json, base64, uuid, time
from io import BytesIO
import os

router = APIRouter()

VIEW_ID = "View #0"

# Thêm thread pool cho blocking operations
executor = ThreadPoolExecutor(max_workers=2)

@router.websocket("/ws/sumo-stream")
async def websocket_sumo_stream(websocket: WebSocket):
    await websocket.accept()
    print("📡 WebSocket client connected")

    selected_junction = None
    last_screenshot_time = 0

    try:
        while True:
            # 1. Nhận message từ FE (chọn junction)
            try:
                message = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                data = json.loads(message)

                if "junction_id" in data:
                    junction_id = str(data["junction_id"]).strip()
                    if junction_id and len(junction_id) < 50:
                        selected_junction = junction_id
                        print(f"🔄 Selected junction: {selected_junction}")

                        # Di chuyển camera
                        try:
                            pos = traci.junction.getPosition(selected_junction)
                            traci.gui.setOffset(VIEW_ID, pos[0], pos[1])
                            traci.gui.setZoom(VIEW_ID, 550)  # Zoom bạn đã chỉnh
                        except Exception as e:
                            print(f"Error moving camera: {e}")

            except asyncio.TimeoutError:
                pass
            except json.JSONDecodeError:
                print("Invalid JSON received")
                continue

            # 2. Thu thập dữ liệu traffic
            vehicle_data = []
            avg_speed = 0.0
            traffic_status = "N/A"

            if selected_junction:
                try:
                    phase = traci.trafficlight.getPhase(selected_junction)
                    traffic_light_info = {
                        "id": selected_junction,
                        "phase": phase
                    }

                    controlled_lanes = traci.trafficlight.getControlledLanes(selected_junction)
                    total_speed = 0.0
                    vehicle_count = 0

                    for lane_id in controlled_lanes:
                        veh_ids = traci.lane.getLastStepVehicleIDs(lane_id)
                        for veh_id in veh_ids:
                            speed = traci.vehicle.getSpeed(veh_id)
                            pos = traci.vehicle.getPosition(veh_id)

                            total_speed += speed
                            vehicle_count += 1

                            vehicle_data.append({
                                "id": veh_id,
                                "position": pos,
                                "speed": speed
                            })

                    avg_speed = total_speed / vehicle_count if vehicle_count > 0 else 0.0

                    if avg_speed < 5:
                        traffic_status = "heavy traffic"
                    elif avg_speed < 15:
                        traffic_status = "moderate traffic"
                    else:
                        traffic_status = "light traffic"

                except Exception as e:
                    traffic_light_info = {
                        "id": selected_junction,
                        "error": f"Junction not found: {e}"
                    }
            else:
                traffic_light_info = {}

            # 3. Gửi data JSON
            await websocket.send_text(json.dumps({
                "type": "data",
                "vehicles": vehicle_data,
                "average_speed": avg_speed,
                "traffic_status": traffic_status,
                "traffic_light": traffic_light_info
            }))

            # 4. Gửi ảnh screenshot (1 FPS)
            current_time = asyncio.get_event_loop().time()
            if current_time - last_screenshot_time >= 1.0:
                try:
                    # Chụp ảnh bằng traci.gui.screenshot
                    temp_file = "temp_sumo_screenshot.png"
                    traci.gui.screenshot(VIEW_ID, temp_file)

                    # Chuyển file ảnh thành base64
                    with open(temp_file, "rb") as f:
                        img_str = base64.b64encode(f.read()).decode("utf-8")

                    # Gửi ảnh lên FE
                    await websocket.send_text(json.dumps({
                        "type": "image",
                        "image": img_str
                    }))

                    # Xóa file tạm để tránh rác
                    os.remove(temp_file)

                    last_screenshot_time = current_time

                except Exception as e:
                    print(f"Screenshot error: {e}")

            # Sleep ngắn để responsive
            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        print("🔌 WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
