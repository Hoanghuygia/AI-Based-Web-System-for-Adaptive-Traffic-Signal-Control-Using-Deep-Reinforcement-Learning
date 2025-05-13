import requests
import time
import pandas as pd
from datetime import datetime, timedelta
from src.model import config
import os

def get_traffic_data(origin_coords, destination_coords, api_key, departure_time):
    """
    Fetch traffic information between two points at a specific time.
    """
    # Convert departure_time to Unix timestamp
    departure_timestamp = int(departure_time.timestamp())

    params = {
        "origin": f"{origin_coords['lat']},{origin_coords['lng']}",
        "destination": f"{destination_coords['lat']},{destination_coords['lng']}",
        "departure_time": departure_timestamp,
        "mode": "driving",
        "alternatives": "false",
        "key": api_key
    }

    try:
        response = requests.get(config.BASE_GOOGLE_MAP_URL, params=params)
        result = response.json()

        if result.get("status") == "OK":
            print('ok')
            leg = result["routes"][0]["legs"][0]
            duration = leg["duration"]["value"]
            distance = leg["distance"]["value"]
            
            # Analyze congestionレベル
            traffic_info = "normal"
            if "duration_in_traffic" in leg:
                traffic_duration = leg["duration_in_traffic"]["value"]
                congestion_factor = traffic_duration / duration
                if congestion_factor > 1.5:
                    traffic_info = "heavy"
                elif congestion_factor > 1.2:
                    traffic_info = "moderate"
            
            return {
                "duration_seconds": duration,
                "distance_meters": distance,
                "traffic_condition": traffic_info
            }
        else:
            print(f"[WARNING] API returned error: {result.get('status')}")
            return None
    except Exception as e:
        print(f"[ERROR] Error calling API: {e}")
        return None

def collect_traffic_data(intersections, api_key, specific_date=None, output_dir="data/traffic"):
    """
    Collect traffic data for bidirectional routes between intersections for a specific day.
    
    Args:
        intersections: Dictionary of intersection coordinates.
        api_key: Google Maps API key.
        specific_date: Datetime object for the day to collect data (default: today).
        output_dir: Directory to save output CSV files (default: data/traffic).
    """
    # List of hours to check: peak and off-peak hours
    hours_to_check = [7, 9, 12, 17, 19, 22]
    count = 0

    intersection_keys = list(intersections.keys())
    
    # Use current date if specific_date is not provided
    if specific_date is None:
        specific_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    data_records = []
    weekday = specific_date.weekday()
    date_str = specific_date.strftime("%Y-%m-%d")
    weekday_str = config.WEEKDAY_MAP[weekday]

    for hour in hours_to_check:
        # Create precise timestamp for each hour
        query_time = specific_date.replace(hour=hour, minute=0, second=0)

        for i, src in enumerate(intersection_keys):
            for j, dst in enumerate(intersection_keys):
                if src == dst:
                    continue  # Skip same point

                result = get_traffic_data(intersections[src], intersections[dst], api_key, query_time)
                count += 1

                if result:
                    data_records.append({
                        "timestamp": query_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "origin": src,
                        "destination": dst,
                        "duration_seconds": result["duration_seconds"],
                        "distance_meters": result["distance_meters"],
                        "traffic_condition": result["traffic_condition"],
                        "day_of_week": weekday,
                        "hour_of_day": hour
                    })
                print('Count: ', count)
                time.sleep(2)  # Avoid API rate limits

    print('Output Dir: ', output_dir)
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save data for the current day
    df = pd.DataFrame(data_records)
    print('After saving')
    filename = f"traffic_data_{weekday_str}_{date_str}.csv"
    filepath = os.path.join(output_dir, filename)
    print('Filename: ', filename)
    print('Path name: ', filepath)
    df.to_csv(filepath, index=False)
    print(f"[INFO] Collected {len(df)} records and saved to {filepath}")

# Example: Run for a specific day
# if __name__ == "__main__":
#     # Example: Collect data for May 13, 2025
#     specific_date = datetime(2025, 5, 13)
#     collect_traffic_data(intersections, config.GOOGLE_MAP_DIRECTIONS_API_KEY, specific_date=specific_date, output_dir="data/traffic")