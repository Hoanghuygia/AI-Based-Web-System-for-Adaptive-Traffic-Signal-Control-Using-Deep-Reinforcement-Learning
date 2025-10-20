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