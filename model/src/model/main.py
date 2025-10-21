import argparse
import pandas as pd
from datetime import datetime
import os
import glob

from src.model import config
from model.utils.map_downloader import download_map
from model.utils.osm_to_sumo import convert_osm_to_net
from model.utils.collect_traffic_data import collect_traffic_data
from model.utils.create_demand_file import create_route_file
from model.utils.create_traffic_light_config import create_traffic_light_config
from model.utils.create_sumo_config_file import create_sumo_config

def download_OSM_file_m(args):
    """
    Download map data by downloading OSM file.
    """
    download_map(coords_dict=args.cord, file_path=args.osm_path, visual_path= args.osm_visual_path)
        
def convert_OSM_to_SUMO_m(args):
    """
    Converting to SUMO network.
    """
    success = convert_osm_to_net(osm_file=args.osm_path, net_file=args.net_file)
    if success:
        print("Convert Successfully!")
    else:
        print("Convert Failed")

def collect_traffic_infor(args):
    """
    Collect traffic information by loading intersections from a CSV file and calling collect_traffic_data.
    """
    # Load intersections from CSV file
    try:
        df = pd.read_csv(args.intersection_path)
        if not all(col in df.columns for col in ['name', 'lat', 'lng']):
            raise ValueError("CSV file must contain 'name', 'lat', and 'lng' columns")
        
        # Convert CSV data to dictionary format: {"name": {"lat": float, "lng": float}}
        intersections = {
            row['name']: {'lat': row['lat'], 'lng': row['lng']}
            for _, row in df.iterrows()
        }
    except FileNotFoundError:
        print(f"[ERROR] Intersection file not found at {args.intersection_path}")
        return
    except Exception as e:
        print(f"[ERROR] Failed to load intersections: {e}")
        return

    # Parse specific_date if provided, otherwise use None (current date)
    specific_date = None
    if args.specific_date:
        try:
            specific_date = datetime.strptime(args.specific_date, "%Y-%m-%d")
        except ValueError:
            print("[ERROR] Invalid specific_date format. Use YYYY-MM-DD (e.g., 2025-05-13)")
            return

    # Call collect_traffic_data
    try:
        collect_traffic_data(
            intersections=intersections,
            api_key=args.api_key,
            specific_date=specific_date,
            output_dir=args.output_dir
        )
    except Exception as e:
        print(f"[ERROR] Failed to collect traffic data: {e}")

def create_demand_file(args):
    """
    Create demand file (.rou.xml) for SUMO simulation.
    
    Args:
        args: ArgumentParser object with net_path, traffic_data_files, mapping_file, out_dir, simulation_period
    """
    # 1. Kiểm tra net file
    if not os.path.exists(args.net_path):
        print(f"[ERROR] Net file not found at {args.net_path}")
        return

    # 2. Đọc mapping file
    try:
        df = pd.read_csv(args.mapping_file)
        if not all(col in df.columns for col in ['Intersection', 'Junction_ID']):
            raise ValueError("CSV file must contain 'Intersection' and 'Junction_ID' columns")
    except FileNotFoundError:
        print(f"[ERROR] Mapping file not found at {args.mapping_file}")
        return
    except Exception as e:
        print(f"[ERROR] Failed to read mapping file: {e}")
        return

    # 3. Lấy danh sách traffic CSV files
    try:
        traffic_data_files = glob.glob(f"{args.traffic_data_files}/*.csv")
        if not traffic_data_files:
            raise FileNotFoundError
    except FileNotFoundError:
        print(f"[ERROR] No traffic CSV files found in directory {args.traffic_data_files}")
        return
    except Exception as e:
        print(f"[ERROR] Failed to load traffic data files: {e}")
        return

    # 4. Gọi hàm tạo route
    try:
        output_file = os.path.join(args.out_dir, "region_1.rou.xml")
        create_route_file(
            net_file=args.net_path,
            traffic_data_files=traffic_data_files,
            mapping_file=args.mapping_file,
            output_file=output_file,
            simulation_period=int(args.simulation_period)
        )
        print("[INFO] Route file created successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to create route file: {e}")

def create_tfl_config(args):
    """
    Create traffic light configuration file (.tl.xml) for SUMO simulation.
    
    Args:
        args: ArgumentParser object with net_file, output_file, tl_type
    """
    # 1. Kiểm tra net file
    if not os.path.exists(args.net_file):
        print(f"[ERROR] Net file not found at {args.net_file}")
        return

    # 2. Gọi hàm tạo traffic light config
    try:
        create_traffic_light_config(
            net_file=args.net_file,
            output_file=args.output_file,
            tl_type=args.tl_type
        )
        print("[INFO] Traffic light configuration file created successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to create traffic light configuration file: {e}")
        
def create_sumo_config_file(args):
    """
    Create SUMO configuration file (.sumocfg) for simulation.
    """
    # 1. Kiểm tra net file
    if not os.path.exists(args.net_file):
        print(f"[ERROR] Net file not found at {args.net_file}")
        return
    # 2. Kiểm tra route file
    if not os.path.exists(args.route_file):
        print(f"[ERROR] Route file not found at {args.route_file}")
        return
    # 3. Kiểm tra traffic light file
    if not os.path.exists(args.traffic_light_file):
        print(f"[ERROR] Traffic light file not found at {args.traffic_light_file}")
        return
    # 4. Gọi hàm tạo SUMO config
    try:
        create_sumo_config(
            net_file=args.net_file,
            route_file=args.route_file,
            traffic_light_file=args.traffic_light_file,
            output_file=args.output_file,
            begin_time=args.begin_time,
            end_time=args.end_time
        )
        print("[INFO] SUMO configuration file created successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to create SUMO configuration file: {e}")

def test(args):
    # test_find_closest_node()
    pass

def main():
    """
    Main function to parse arguments and execute commands.
    """
    # ================================================
    # Optional: Check GPU and Torch (uncomment if needed)
    # ================================================
    # print("PyTorch version:", torch.__version__)
    # print("CUDA available:", torch.cuda.is_available())
    # print("CUDA version:", torch.version.cuda)
    # print("GPU name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU found")

    # ================================================
    # Argument Parser Setup
    # ================================================
    parser = argparse.ArgumentParser(
        description="Model to optimize traffic light signal"
    )
    subparser = parser.add_subparsers(dest="command", help="Command to run")
    
    # ------------------------------------------------
    # Subparser: download_osm_map
    # ------------------------------------------------
    collect_parser = subparser.add_parser(
        "download_osm_map", help="Collect data map for model"
    )
    collect_parser.add_argument(
        "--cord", type=str, default=config.OSM_CORDINATOR, help="Coordinator / BBOx of map"
    )
    collect_parser.add_argument(
        "--osm-path", type=str, default=config.OSM_PATH, help="Path to save OSM file"
    )
    collect_parser.add_argument(
        "--osm-visual-path", type=str, default=config.VISUAL_OSM_PATH, help="Visual file"
    )

    # ------------------------------------------------
    # Subparser: convert_OSM_to_SUMO
    # ------------------------------------------------
    collect_parser = subparser.add_parser(
        "convert_OSM_to_SUMO", help="Convert OSM file to .net.xml file"
    )
    collect_parser.add_argument(
        "--osm-path", type=str, default=config.OSM_PATH, help="Path to OSM file"
    )
    collect_parser.add_argument(
        "--net-file", type=str, default=config.NET_FILE_PATH, help="Path to SUMO network file"
    )


    # ------------------------------------------------
    # Subparser: collect_traffic
    # ------------------------------------------------
    collect_traffic_parser = subparser.add_parser(
        'collect_traffic', help="Collect traffic data"
    )
    collect_traffic_parser.add_argument(
        '--intersection-path',
        type=str,
        default=config.INTERSECTION_DATA_FILE,
        help="Path to intersection list CSV file (default: config.INTERSECTION_DATA_FILE)"
    )
    collect_traffic_parser.add_argument(
        '--specific-date',
        type=str,
        default=None,
        help="Specific date for data collection in YYYY-MM-DD format (default: current date)"
    )
    collect_traffic_parser.add_argument(
        '--output-dir',
        type=str,
        default="data/traffic",
        help="Directory to save traffic data CSV files (default: data/traffic)"
    )
    collect_traffic_parser.add_argument(
        '--api-key',
        type=str,
        default=getattr(config, 'GOOGLE_MAP_DIRECTIONS_API_KEY', 'your_api_key_here'),
        help="Google Maps API key (default: config.GOOGLE_MAPS_API_KEY or placeholder)"
    )

    # ------------------------------------------------
    # Subparser: create_demand
    # ------------------------------------------------
    create_demand = subparser.add_parser(
        'create_demand', help="Create demand file"
    )
    create_demand.add_argument(
        '--net-path',
        type=str,
        default="src/model/sumo_files/network/region_1.net.xml",
        help="Path to net file"
    )
    create_demand.add_argument(
        '--traffic-data-files',
        type=str,
        default="src/model/data/traffic",
        help="Folder containing traffic data CSV files"
    )
    create_demand.add_argument(
        '--mapping-file',
        type=str,
        default="src/model/data/intersections/intersection_mapping.csv",
        help="CSV file with intersection mapping list"
    )
    create_demand.add_argument(
        '--out-dir',
        type=str,
        default="src/model/sumo_files/routes/region_1.rou.xml",
        help="Output route file path"
    )
    create_demand.add_argument(
        '--simulation-period',
        type=str,
        default=259200,
        help="Simulation time in seconds (default = 3 days)"
    )
    # ------------------------------------------------
    # Subparser: create traffic light config command
    # ------------------------------------------------
    create_tl_config = subparser.add_parser(
        'create_tl_config', help="Create traffic light configuration file"
    )
    create_tl_config.add_argument(
        '--net-file',
        type=str,
        default="src/model/sumo_files/network/region_1.net.xml",
        help="Path to net file"
    )
    create_tl_config.add_argument(
        '--output-file',
        type=str,
        default="src/model/sumo_files/traffic_lights/region_1.tl.xml",
        help="Output traffic light config file path"
    )
    create_tl_config.add_argument(
        '--tl-type',
        type=str,
        default="static",
        help="Traffic light type (default: static)"
    )
    # ------------------------------------------------
    # Subparser: create sumo config command
    # ------------------------------------------------
    create_sumo_config = subparser.add_parser(
        'create_sumo_config', help="Create SUMO configuration file"
    )
    create_sumo_config.add_argument(
        '--net-file',
        type=str,
        default="src/model/sumo_files/network/region_1.net.xml",
        help="Path to net file"
    )
    create_sumo_config.add_argument(
        '--route-file',
        type=str,
        default="src/model/sumo_files/routes/region_1.rou.xml",
        help="Path to route file"
    )
    create_sumo_config.add_argument(
        '--traffic-light-file',
        type=str,
        default="src/model/sumo_files/traffic_lights/region_1.tl.xml",
        help="Path to traffic light file"
    )
    create_sumo_config.add_argument(
        '--output-file',
        type=str,
        default="src/model/sumo_files/region_1.sumocfg",
        help="Path to output SUMO config file"
    )
    create_sumo_config.add_argument(
        '--begin-time',
        type=int,
        default=0,
        help="Begin time for simulation (default: 0)"
    )
    create_sumo_config.add_argument(
        '--end-time',
        type=int,
        default=3600,
        help="End time for simulation (default: 3600)"
    )
    # ------------------------------------------------
    # Subparser: test command
    # ------------------------------------------------
    test_command = subparser.add_parser(
        'test', help="Create demand file"
    )

    # ================================================
    # Parse Arguments and Execute
    # ================================================
    args = parser.parse_args()

    if args.command == "download_osm_map":
        download_OSM_file_m(args)
    if args.command == "convert_OSM_to_SUMO":
        convert_OSM_to_SUMO_m(args)
    elif args.command == "collect_traffic":
        collect_traffic_infor(args)
    elif args.command == "create_demand":
        create_demand_file(args)
    elif args.command == "create_tl_config":
        create_tfl_config(args)
    elif args.command == "create_sumo_config":
        create_sumo_config_file(args)
    elif args.command == "test":
        test(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
