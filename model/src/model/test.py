import pandas as pd
from pyproj import Transformer

# Tạo transformer từ WGS84 (EPSG:4326) sang UTM zone 48N (EPSG:32648)
transformer = Transformer.from_crs("EPSG:4326", "+proj=utm +zone=48 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

# Đọc file CSV đầu vào
df = pd.read_csv("src/model/data/intersections/intersection_list.csv")

# Chuyển đổi từng dòng sang UTM
def convert_row(row):
    x, y = transformer.transform(row['lat'], row['lng'])  # lat, lng => x, y
    return pd.Series({'x': x, 'y': y})

# Áp dụng chuyển đổi và ghép vào DataFrame ban đầu
utm_coords = df.apply(convert_row, axis=1)
df = pd.concat([df, utm_coords], axis=1)

# Xuất ra file CSV mới
df.to_csv("src/model/data/intersections/intersection_list_utm.csv", index=False)

print("Chuyển đổi hoàn tất. Kết quả được lưu vào 'output_with_utm.csv'")
