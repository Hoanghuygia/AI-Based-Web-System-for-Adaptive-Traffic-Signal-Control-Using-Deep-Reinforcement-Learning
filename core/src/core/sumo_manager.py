import traci
import subprocess

class SUMOManager:
    def __init__(self, sumo_cfg_path: str, sumo_binary="sumo-gui", port=8813):
        self.sumo_cfg_path = sumo_cfg_path
        self.sumo_binary = sumo_binary
        self.port = port
        self.process = None
        self.running = False

    def start(self):
        if self.running:
            print("SUMO already running.")
            return

        sumo_cmd = [self.sumo_binary, "-c", self.sumo_cfg_path, "--remote-port", str(self.port)]
        self.process = subprocess.Popen(sumo_cmd)
        traci.init(self.port)
        self.running = True
        print("SUMO started and connected via TraCI.")

    def stop(self):
        if self.running:
            traci.close()
            self.process.terminate()
            self.running = False
            print("SUMO stopped.")

    def step(self):
        if self.running:
            traci.simulationStep()

    def is_running(self):
        return self.running
