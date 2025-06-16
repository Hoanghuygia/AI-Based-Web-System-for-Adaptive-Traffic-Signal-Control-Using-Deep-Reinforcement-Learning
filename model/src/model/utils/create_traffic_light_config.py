import os
import xml.etree.ElementTree as ET
import sumolib

def create_traffic_light_config(net_file, output_file, tl_type="static"):
    """
    Generate a traffic light configuration file (.add.xml) from a network file (.net.xml).
    Parameters:
        net_file (str): Path to the .net.xml file.
        output_file (str): Path to save the .add.xml file.
        tl_type (str): Traffic light control type (static, actuated, RL).
    """
    # 1. Check input file
    if not os.path.exists(net_file):
        raise FileNotFoundError(f"Network file not found: {net_file}")
   
    # 2. Read network file
    net = sumolib.net.readNet(net_file)
    
    # 3. Create root element
    additional = ET.Element("additional")
    
    # 4. Get intersections with traffic lights
    traffic_light_nodes = net.getTrafficLights()
    if not traffic_light_nodes:
        print("⚠️ No traffic lights found in the network.")
        return
   
    # 5. Iterate through each traffic light
    for tl in traffic_light_nodes:
        tl_id = tl.getID()
        programs = [create_default_program(tl)]
        
        # Create tlLogic element for each program
        for program_id, program in enumerate(programs):
            tlLogic = ET.SubElement(additional, "tlLogic")
            tlLogic.set("id", tl_id)
            tlLogic.set("type", tl_type)
            tlLogic.set("programID", str(program_id) if len(programs) > 1 else "0")
            tlLogic.set("offset", "0")
            
            # Add phases
            phases = program.getPhases()
            for phase in phases:
                phase_elem = ET.SubElement(tlLogic, "phase")
                
                duration = phase.duration
                state = phase.state
                
                phase_elem.set("duration", str(duration))
                phase_elem.set("state", state)
                
                # Set minDur and maxDur for adaptive control
                if tl_type in ["actuated", "RL"]:
                    phase_elem.set("minDur", "7")
                    phase_elem.set("maxDur", "120")
    
    # 6. Write XML file using ElementTree
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    tree = ET.ElementTree(additional)
    ET.indent(tree.getroot(), space="  ")  # Add pretty printing (Python 3.9+)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    
    print(f"✅ Traffic light configuration file created: {output_file}")

def create_default_program(tl):
    """Create a default program for traffic light if none exists"""
    class DefaultProgram:
        def __init__(self, phases):
            self._phases = phases
        
        def getPhases(self):
            return self._phases
    
    phases = create_default_phases(tl)
    return DefaultProgram(phases)

def create_default_phases(tl):
    """Create default phases for a traffic light based on its connections"""
    class DefaultPhase:
        def __init__(self, duration, state):
            self.duration = duration
            self.state = state
    
    # Get number of connections/links
    connections = tl.getConnections()
    print("Connections length:", len(connections))
    num_links = len(connections) if connections else 4  # Default to 4 if no connections
    print("Number of links:", num_links)
    
    # Create basic 2-phase system (green for main directions, then perpendicular)
    # This is a simplified approach - you may need to adjust based on your network
    state_length = max(num_links, 4)  # Ensure minimum state length
    
    # Phase 1: Main direction green (assuming first half of connections)
    state1 = "G" * (state_length // 2) + "r" * (state_length - state_length // 2)
    # Phase 2: Perpendicular direction green
    state2 = "r" * (state_length // 2) + "G" * (state_length - state_length // 2)
    
    phases = [
        DefaultPhase(30, state1),  # Green for main direction
        DefaultPhase(3, state1.replace('G', 'y')),   # Yellow for main direction
        DefaultPhase(30, state2),  # Green for perpendicular direction  
        DefaultPhase(3, state2.replace('G', 'y'))    # Yellow for perpendicular direction
    ]
    
    return phases

def create_default_state(tl):
    """Create a default state string for a traffic light"""
    connections = tl.getConnections()
    num_links = len(connections) if connections else 4
    return "G" * max(num_links, 4)  # All green as default

def create_rl_traffic_light_config(net_file, output_file):
    """
    Create traffic light configuration specifically optimized for Reinforcement Learning
    """
    return create_traffic_light_config(net_file, output_file, tl_type="static")
