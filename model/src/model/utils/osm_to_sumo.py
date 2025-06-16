# import subprocess
# import os

# def convert_osm_to_net(osm_file, net_file):
#     os.makedirs(os.path.dirname(net_file), exist_ok=True)
    
#     # cmd = [
#     #     'netconvert',
#     #     '--osm', osm_file,
#     #     '--output', net_file,
#     #     '--geometry.remove', 'true',
#     #     '--roundabouts.guess', 'true',
#     #     '--tls.guess', 'true',
#     #     '--tls.discard-simple', 'false',
#     #     '--tls.join', 'true',
#     #     '--tls.guess-signals', 'true',
#     #     '--junctions.join', 'true',
#     #     '--ramps.guess', 'true',
#     #     '--edges.join', 'true',
#     #     '--remove-edges.isolated', 'true',
#     #     '--no-turnarounds', 'true',
#     #     '--sidewalks.guess', 'true',
#     #     '--crossings.guess', 'true',
#     #     '--lefthand', 'false',
#     #     '--verbose', 'true',
#     # ]
    
#     cmd = [
#         'netconvert',
#         '--osm', osm_file,
#         '--output', net_file,
#         '--proj.scale', '1.0',
#         '--proj.utm', 'false',  
#         '--roundabouts.guess', 'true',
#         '--tls.guess', 'true',
#         '--tls.discard-simple', 'false',
#         '--tls.join', 'true',
#         '--tls.guess-signals', 'true',
#         '--ramps.guess', 'true',
#         '--no-turnarounds', 'true',
#         '--sidewalks.guess', 'true',
#         '--crossings.guess', 'true',
#         '--lefthand', 'false',
#         '--verbose', 'true',
#     ]

#     process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout, stderr = process.communicate()

#     print("STDOUT:", stdout.decode())
#     if stderr:
#         print("STDERR:", stderr.decode())

#     return process.returncode == 0

import subprocess
import os

def convert_osm_to_net(osm_file, net_file):
    os.makedirs(os.path.dirname(net_file), exist_ok=True)
    cmd = [
        'netconvert',
        '--osm', osm_file,
        '--output', net_file,
        '--proj.utm', 'true', 
        '--roundabouts.guess', 'true',
        '--tls.guess', 'true',
        '--tls.discard-simple', 'false',
        '--tls.join', 'true',
        '--tls.guess-signals', 'true',
        '--ramps.guess', 'true',
        '--no-turnarounds', 'true',
        '--sidewalks.guess', 'true',
        '--crossings.guess', 'true',
        '--lefthand', 'false',
        '--verbose', 'true',
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print("STDOUT:", stdout.decode())
    if stderr:
        print("STDERR:", stderr.decode())
    return process.returncode == 0
