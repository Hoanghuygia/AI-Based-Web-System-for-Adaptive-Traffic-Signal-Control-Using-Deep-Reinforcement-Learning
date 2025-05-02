from model.utils.map_downloader import download_map
from model.utils.osm_to_sumo import convert_osm_to_net

def main():
    download_map()
    success = convert_osm_to_net(
        osm_file='src/model/data/map/region_1.osm',
        net_file='src/model/sumo_files/network/quan_1.net.xml'
    )
    if success:
        print("Convert Successfully!")
    else:
        print("Convert Failed")

if __name__ == "__main__":
    main()
