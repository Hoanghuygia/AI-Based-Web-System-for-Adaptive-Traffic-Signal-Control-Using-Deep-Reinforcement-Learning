import argparse
import pandas as pd
from datetime import datetime
import os

from src.model import config
from model.utils.map_downloader import download_map
from model.utils.osm_to_sumo import convert_osm_to_net
from model.utils.collect_traffic_data import collect_traffic_data


def collect_map_data(args):
    """
    Collect map data by downloading OSM file and converting to SUMO network.
    """
    download_map(savePath=args.map_image_chart)
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
        
import pandas as pd
import glob
import os
import sys
from datetime import datetime

def create_route_file(net_file, traffic_data_files, intersection_file, output_file, simulation_period):
    # Giả sử bạn đã định nghĩa đầy đủ hàm này
    pass

def create_demand_file(args):
    # 1. Kiểm tra net file
    if not os.path.exists(args.net_path):
        print(f"[ERROR] Net file not found at {args.net_path}")
        return

    # 2. Đọc intersection file
    try:
        df = pd.read_csv(args.intersection_file)
        if not all(col in df.columns for col in ['name', 'lat', 'lng']):
            raise ValueError("CSV file must contain 'name', 'lat', and 'lng' columns")
    except FileNotFoundError:
        print(f"[ERROR] Intersection file not found at {args.intersection_file}")
        return
    except Exception as e:
        print(f"[ERROR] Failed to read intersection file: {e}")
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

    # 5. Gọi hàm tạo route
    try:
        create_route_file(
            net_file=args.net_path,
            traffic_data_files=traffic_data_files,
            intersection_file=args.intersection_file,
            output_file=args.out_dir,
            simulation_period=int(args.simulation_period)
        )
        print("[INFO] Route file created successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to create route file: {e}")

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
    # Subparser: collect_data_map
    # ------------------------------------------------
    collect_parser = subparser.add_parser(
        "collect_data_map", help="Collect data map for model"
    )
    collect_parser.add_argument(
        "--osm-path", type=str, default=config.DISTRICT_1_OSM, help="Path to OSM file"
    )
    collect_parser.add_argument(
        "--net-file", type=str, default=config.DISTRICT_1_NET, help="Path to SUMO network file"
    )
    collect_parser.add_argument(
        "--map-image-chart",
        type=str,
        default=config.DISTRICT_1_TRAFFIC_CHART,
        help="Path to traffic chart image",
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
        '--intersection-file',
        type=str,
        default="src/model/data/traffic/intersection_list.csv",
        help="CSV file with intersection list"
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

    # ================================================
    # Parse Arguments and Execute
    # ================================================
    args = parser.parse_args()

    if args.command == "collect_data_map":
        collect_map_data(args)
    elif args.command == "collect_traffic":
        collect_traffic_infor(args)
    elif args.command == "create_demand":
        create_demand_file(args)
    else:
        parser.print_help()


# ================================================
# Entry Point
# ================================================
if __name__ == "__main__":
    main()
