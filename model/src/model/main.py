import argparse

from model.utils.map_downloader import download_map
from model.utils.osm_to_sumo import convert_osm_to_net
from src.model import config

def collect_map_data(args):
    download_map(savePath=args.map_image_chart)
    success = convert_osm_to_net(
        osm_file=args.osm_path,
        net_file=args.net_file
    )
    if success:
        print("Convert Successfully!")
    else:
        print("Convert Failed")
    

def main():
    # check GPU and Torch
    # print("PyTorch version:", torch.__version__)
    # print("CUDA available:", torch.cuda.is_available())
    # print("CUDA version:", torch.version.cuda)
    # print("GPU name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU found")
    parser = argparse.ArgumentParser(description= "Model to optimize traffic light signal")
    subparser = parser.add_subparsers(dest='command', help= 'Command to run')
    
    # Collect data map parser
    collect_parser = subparser.add_parser('collect_data_map', help="Collect data map for model")
    collect_parser.add_argument('--osm-path', type=str, default=config.DISTRICT_1_OSM, help="Path to file osm")
    collect_parser.add_argument('--net-file', type=str, default=config.DISTRICT_1_NET, help="Path to sumo file")
    collect_parser.add_argument('--map-image-chart', type=str, default=config.DISTRICT_1_TRAFFIC_CHART, help="Path to traffic chart")
    
    args = parser.parse_args()
    
    if args.command == 'collect_data_map':
        collect_map_data(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
