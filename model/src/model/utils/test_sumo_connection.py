# test_sumo_connection.py
import traci
import sumolib

def test_sumo_connection():
    # Đường dẫn đến các file SUMO của bạn
    sumo_binary = sumolib.checkBinary('sumo')
    sumo_cmd = [sumo_binary, "-c", "../sumo_files/region_1.sumocfg"]
    
    traci.start(sumo_cmd)
    print("SUMO started successfully")
    
    # Test basic commands
    step = 0
    while step < 10:
        traci.simulationStep()
        step += 1
        print(f"Step: {step}")
    
    traci.close()
    print("SUMO connection test completed")

if __name__ == "__main__":
    test_sumo_connection()