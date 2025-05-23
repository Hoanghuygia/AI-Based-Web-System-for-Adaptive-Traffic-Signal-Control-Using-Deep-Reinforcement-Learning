import pandas as pd
import xml.etree.ElementTree as ET
import math
import numpy as np

def parse_net_xml(net_file):
    """Parse SUMO net.xml file to extract junction coordinates"""
    tree = ET.parse(net_file)
    root = tree.getroot() 
    
    # Get network offset and conversion parameters
    location = root.find('location')
    net_offset = location.get('netOffset').split(',')
    net_offset_x = float(net_offset[0])
    net_offset_y = float(net_offset[1])
    
    # Get original boundary for coordinate conversion
    orig_boundary = location.get('origBoundary').split(',')
    orig_min_lon = float(orig_boundary[0])
    orig_min_lat = float(orig_boundary[1])
    orig_max_lon = float(orig_boundary[2])
    orig_max_lat = float(orig_boundary[3])
    
    # Get conversion boundary  
    conv_boundary = location.get('convBoundary').split(',')
    conv_min_x = float(conv_boundary[0])
    conv_min_y = float(conv_boundary[1])
    conv_max_x = float(conv_boundary[2])
    conv_max_y = float(conv_boundary[3])
    
    # Extract junctions
    junctions = {}
    for junction in root.findall('junction'):
        junction_id = junction.get('id')
        x = float(junction.get('x'))
        y = float(junction.get('y'))
        
        # Convert SUMO coordinates back to lat/lon
        # Add the network offset back
        utm_x = x - net_offset_x
        utm_y = y - net_offset_y
        
        # Simple linear interpolation to convert back to lat/lon
        # This is an approximation - for precise conversion you'd need the exact UTM projection
        lon_ratio = (x - conv_min_x) / (conv_max_x - conv_min_x)
        lat_ratio = (y - conv_min_y) / (conv_max_y - conv_min_y)
        
        estimated_lon = orig_min_lon + lon_ratio * (orig_max_lon - orig_min_lon)
        estimated_lat = orig_min_lat + lat_ratio * (orig_max_lat - orig_min_lat)
        
        junctions[junction_id] = {
            'sumo_x': x,
            'sumo_y': y,
            'estimated_lat': estimated_lat,
            'estimated_lon': estimated_lon
        }
    
    return junctions

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points on Earth (in meters)"""
    R = 6371000  # Earth's radius in meters
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def validate_intersection_mapping(net_file, intersection_file, mapping_file):
    """Validate the intersection mapping by comparing coordinates"""
    
    print("🔍 Starting mapping validation...")
    print("=" * 60)
    
    # Load data
    junctions = parse_net_xml(net_file)
    intersections_df = pd.read_csv(intersection_file)
    mapping_df = pd.read_csv(mapping_file)
    
    print(f"📊 Statistics:")
    print(f"   - Number of junctions in net.xml: {len(junctions)}")
    print(f"   - Number of intersections in intersection_list.csv: {len(intersections_df)}")
    print(f"   - Number of mappings in intersection_mapping.csv: {len(mapping_df)}")
    print()
    
    # Validate mappings
    results = []
    errors = []
    
    for _, row in mapping_df.iterrows():
        intersection_name = row['Intersection']
        junction_id = str(row['Junction_ID'])
        
        # Find intersection coordinates
        intersection_row = intersections_df[intersections_df['name'] == intersection_name]
        if intersection_row.empty:
            errors.append(f"❌ Intersection '{intersection_name}' not found in intersection_list.csv")
            continue
        
        real_lat = intersection_row['lat'].iloc[0]
        real_lon = intersection_row['lng'].iloc[0]
        
        # Find junction coordinates
        if junction_id not in junctions:
            errors.append(f"❌ Junction ID '{junction_id}' not found in net.xml")
            continue
        
        junction_data = junctions[junction_id]
        estimated_lat = junction_data['estimated_lat']
        estimated_lon = junction_data['estimated_lon']
        
        # Calculate distance difference
        distance = haversine_distance(real_lat, real_lon, estimated_lat, estimated_lon)
        
        results.append({
            'intersection_name': intersection_name,
            'junction_id': junction_id,
            'real_lat': real_lat,
            'real_lon': real_lon,
            'estimated_lat': estimated_lat,
            'estimated_lon': estimated_lon,
            'distance_error_m': distance,
            'sumo_x': junction_data['sumo_x'],
            'sumo_y': junction_data['sumo_y']
        })
    
    # Print errors
    if errors:
        print("🚨 Errors found:")
        for error in errors:
            print(f"   {error}")
        print()
    
    # Analyze results
    if results:
        results_df = pd.DataFrame(results)
        
        print("📈 Analysis Results:")
        print(f"   - Number of valid mappings: {len(results)}")
        print(f"   - Average distance error: {results_df['distance_error_m'].mean():.2f} m")
        print(f"   - Median distance error: {results_df['distance_error_m'].median():.2f} m")
        print(f"   - Maximum distance error: {results_df['distance_error_m'].max():.2f} m")
        print(f"   - Minimum distance error: {results_df['distance_error_m'].min():.2f} m")
        print()
        
        # Classify accuracy
        very_good = len(results_df[results_df['distance_error_m'] <= 50])
        good = len(results_df[(results_df['distance_error_m'] > 50) & (results_df['distance_error_m'] <= 100)])
        acceptable = len(results_df[(results_df['distance_error_m'] > 100) & (results_df['distance_error_m'] <= 200)])
        poor = len(results_df[results_df['distance_error_m'] > 200])
        
        print("🎯 Accuracy Assessment:")
        print(f"   - Very Good (≤50m): {very_good} mappings ({very_good/len(results)*100:.1f}%)")
        print(f"   - Good (50-100m): {good} mappings ({good/len(results)*100:.1f}%)")
        print(f"   - Acceptable (100-200m): {acceptable} mappings ({acceptable/len(results)*100:.1f}%)")
        print(f"   - Poor (>200m): {poor} mappings ({poor/len(results)*100:.1f}%)")
        print()
        
        # Show detailed results
        print("📋 Detailed Mapping Results:")
        print("-" * 120)
        print(f"{'Intersection':<40} {'Junction ID':<12} {'Real Lat':<10} {'Real Lon':<11} {'Est Lat':<10} {'Est Lon':<11} {'Error(m)':<8}")
        print("-" * 120)
        
        # Sort by error distance
        results_df_sorted = results_df.sort_values('distance_error_m')
        
        for _, row in results_df_sorted.iterrows():
            status = "✅" if row['distance_error_m'] <= 100 else "⚠️" if row['distance_error_m'] <= 200 else "❌"
            print(f"{row['intersection_name']:<40} {row['junction_id']:<12} {row['real_lat']:<10.6f} {row['real_lon']:<11.6f} {row['estimated_lat']:<10.6f} {row['estimated_lon']:<11.6f} {row['distance_error_m']:<8.1f} {status}")
        
        print()
        
        # Recommendations
        print("💡 Recommendations:")
        if results_df['distance_error_m'].mean() <= 100:
            print("   ✅ Your mappings show good accuracy for SUMO simulation.")
        elif results_df['distance_error_m'].mean() <= 200:
            print("   ⚠️ Mappings are acceptable but may require review for some points.")
        else:
            print("   ❌ Mappings need improvement; there might be errors in the mapping process.")
        
        if poor > 0:
            print(f"   🔍 You should review {poor} mappings with errors greater than 200m.")
        
        return results_df
    
    else:
        print("❌ No valid mappings to analyze.")
        return None

# Main execution
if __name__ == "__main__":
    # File paths
    net_file = "src/model/sumo_files/network/region_1.net.xml"
    intersection_file = "src/model/data/intersections/intersection_list.csv"
    mapping_file = "src/model/data/intersections/intersection_mapping.csv"
    
    # Run validation
    results = validate_intersection_mapping(net_file, intersection_file, mapping_file)
    
    if results is not None:
        # Save detailed results to CSV
        output_file = "intersection_mapping_validation_results.csv"
        results.to_csv(output_file, index=False)
        print(f"\n📄 Detailed results saved to: {output_file}")