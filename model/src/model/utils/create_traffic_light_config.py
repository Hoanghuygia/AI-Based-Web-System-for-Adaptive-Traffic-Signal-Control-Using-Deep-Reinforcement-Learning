import os 
import xml.etree.ElementTree as ET 
import xml.dom.minidom as minidom 
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
    
    # 5. Iterate through each traffic light and get the default program
    for tl in traffic_light_nodes:
        tl_id = tl.getID()
        program = tl.getProgram()  # Get default program

        # Create tlLogic element
        tlLogic = ET.SubElement(additional, "tlLogic")
        tlLogic.set("id", tl_id)
        tlLogic.set("type", tl_type)
        tlLogic.set("programID", "default")
        tlLogic.set("offset", "0")

        # Get phases in the program
        for phase in program.getPhases():
            phase_elem = ET.SubElement(tlLogic, "phase")
            phase_elem.set("duration", str(phase.duration))
            phase_elem.set("state", phase.state)

            # 6. Check and set minDur and maxDur if they exist
            if hasattr(phase, "minDur") and phase.minDur > 0:
                phase_elem.set("minDur", 7)
            if hasattr(phase, "maxDur") and phase.maxDur > 0:
                phase_elem.set("maxDur", 40)

    # 7. Write XML file with pretty formatting
    xml_str = ET.tostring(additional, encoding='utf-8')
    parsed = minidom.parseString(xml_str)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(parsed.toprettyxml(indent="  "))

    print(f"✅ Traffic light configuration file created: {output_file}")