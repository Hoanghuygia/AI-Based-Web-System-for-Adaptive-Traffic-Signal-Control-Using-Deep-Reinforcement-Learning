# src/api/endpoints/ws_sumo.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import traci
import asyncio
import json
import base64
from io import BytesIO
import pyautogui

router = APIRouter()

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


@router.websocket("/ws/sumo")
async def websocket_sumo_data(websocket: WebSocket):
    await websocket.accept()
    print("📡 WebSocket client connected")

    selected_junction = None  # mặc định chưa có junction nào được chọn

    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                data = json.loads(message)
                if "junction_id" in data:
                    selected_junction = data["junction_id"]
                    print(f"🔄 Selected junction: {selected_junction}")
            except asyncio.TimeoutError:
                pass

            vehicle_data = []
            avg_speed = 0.0
            traffic_status = "N/A"  # Default

            if selected_junction:
                try:
                    # Thông tin traffic light
                    phase = traci.trafficlight.getPhase(selected_junction)
                    traffic_light_info = {
                        "id": selected_junction,
                        "phase": phase
                    }

                    # Các làn được điều khiển bởi junction này
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

                    # Tính tốc độ trung bình
                    avg_speed = total_speed / vehicle_count if vehicle_count > 0 else 0.0

                    # Phân loại giao thông
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

            # Gửi dữ liệu về frontend
            await websocket.send_text(json.dumps({
                "vehicles": vehicle_data,
                "average_speed": avg_speed,
                "traffic_status": traffic_status,
                "traffic_light": traffic_light_info
            }))

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("🔌 WebSocket client disconnected")



@router.websocket("/ws/sumo-image")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            screenshot = pyautogui.screenshot()  # Capture toàn màn hình
            # Nếu bạn chỉ muốn phần SUMO-GUI: 
            # screenshot = pyautogui.screenshot(region=(x, y, w, h))

            buffer = BytesIO()
            screenshot.save(buffer, format="JPEG")
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

            await websocket.send_text(img_str)
            await asyncio.sleep(1)  # Gửi mỗi 1 giây
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

# @router.websocket("/ws/sumo-image")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             # Capture chỉ màn hình phụ (phía bên phải)
#             screenshot = pyautogui.screenshot(region=(1920, 0, 2560, 1600))

#             buffer = BytesIO()
#             screenshot.save(buffer, format="JPEG")
#             img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

#             await websocket.send_text(img_str)
#             await asyncio.sleep(1)  # Gửi mỗi 1 giây
#     except Exception as e:
#         print(f"WebSocket error: {e}")
#         await websocket.close()