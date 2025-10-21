import subprocess
import os

def convert_osm_to_net(osm_file, net_file):
    os.makedirs(os.path.dirname(net_file), exist_ok=True)
    cmd = [
        'netconvert',
        '--osm', osm_file,
        '--output', net_file,

        # --- Basic Configuration ---
        '--proj.utm','true',                       # Use default UTM projection
        '--ramps.guess', 'true',
        '--no-turnarounds', 'true',
        '--remove-edges.isolated', 'true',
        '--default.speed', '16.67',     

        # --- Traffic lights (TLS) ---
        '--tls.guess-signals', 'true',      # Automatically guess traffic signals
        '--tls.discard-simple', 'false',    # Keep even simple traffic lights
        '--tls.join', 'false',              # Do not join traffic lights (for MARL simulation)
        '--tls.default-type', 'static',     # Default traffic light type: static (for RL control)
        '--tls.allred.time', '2',           # All-red transition time

        # --- Geometry & Display ---
        '--geometry.remove', 'true',
        '--geometry.max-angle', '10',
        '--roundabouts.guess', 'true',
        '--junctions.join', 'true',

        '--verbose', 'true'
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print("STDOUT:", stdout.decode())
    if stderr:
        print("STDERR:", stderr.decode())
    return process.returncode == 0