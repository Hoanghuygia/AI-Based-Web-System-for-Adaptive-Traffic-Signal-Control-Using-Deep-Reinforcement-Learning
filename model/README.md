### Guide to run
## Download the map
# Run default setting
```bash
poetry run python -m model.main download_osm_map
```

# Run with specific parameters
```bash
poetry run python -m model.main download_osm_map --cord "10.9804,106.6752,11.0804,106.7752" --osm-path "./data/map.osm" --osm-visual-path "./data/visual_map.png"
```

## Parameters
- `--cord`: Coordinator / BBox of map (default: value from config.OSM_CORDINATOR)
  - Format: "min_lat,min_lon,max_lat,max_lon"
  - Example: "10.9804,106.6752,11.0804,106.7752"
- `--osm-path`: Path to save OSM file (default: value from config.OSM_PATH)
  - Example: "./data/map.osm"
- `--osm-visual-path`: Path to save visualization file (default: value from config.VISUAL_OSM_PATH)
  - Example: "./data/visual_map.png"

## Example usage
```bash
# Download map with custom coordinates
poetry run python -m model.main download_osm_map --cord "10.9804,106.6752,11.0804,106.7752"

# Download map and save to specific location
poetry run python -m model.main download_osm_map --osm-path "./custom/path/map.osm"

# Download map with all custom parameters
poetry run python -m model.main download_osm_map \
  --cord "10.9804,106.6752,11.0804,106.7752" \
  --osm-path "./data/my_map.osm" \
  --osm-visual-path "./data/my_visual.png"
```

## Convert OSM to SUMO Network
# Run default setting
```bash
poetry run python -m model.main convert_OSM_to_SUMO
```
# Run with specific parameters
```bash
poetry run python -m model.main convert_OSM_to_SUMO --osm-path "./data/map.osm" --net-file "./data/network.net.xml"
```
## Parameters
- `--osm-path`: Path to OSM file (default: value from config.OSM_PATH)
  - Example: "./data/map.osm"
- `--net-file`: Path to save SUMO network file (default: value from config.NET_FILE_PATH)
  - Example: "./data/network.net.xml"
## Example usage
```bash
# Convert OSM to SUMO network with default settings
poetry run python -m model.main convert_OSM_to_SUMO

# Convert with custom OSM file path
poetry run python -m model.main convert_OSM_to_SUMO --osm-path "./custom/map.osm"

# Convert with custom output network file
poetry run python -m model.main convert_OSM_to_SUMO --net-file "./output/my_network.net.xml"

# Convert with all custom parameters
poetry run python -m model.main convert_OSM_to_SUMO \
  --osm-path "./data/my_map.osm" \
  --net-file "./data/my_network.net.xml"
```