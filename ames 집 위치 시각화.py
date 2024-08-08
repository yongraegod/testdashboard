!pip install folium
import pandas as pd
import folium

# Ames 데이터 불러오기
df = pd.read_csv("../lsbigdata-project1/data/houseprice-with-lonlat.csv")
df

df.columns

ames_df = df[["Longitude", "Latitude"]]

# ames 중심 위도, 경도 구하기
ames_df['Longitude'].mean()
ames_df['Latitude'].mean()

# 흰 도화지 맵 그리기
ames_map = folium.Map(location = [42.034, -93.642],
                    zoom_start = 12,
                    tiles='cartodbpositron')
ames_map.save('maps/ames_map.html')

# 점 찍는 법
folium.Marker([42.034, -93.642]).add_to(ames_map)
ames_map.save('ames_map.html')

# for 문을 사용해서 전체 집의 위치를 마커로 찍기    
for lat, lon in zip (ames_df['Latitude'], ames_df['Longitude']):
      folium.Marker([lat, lon]).add_to(ames_map)
      
ames_map.save('maps/ames_map.html')
-------------------------------
# 방법 2
from folium.plugins import MarkerCluster

# 데이터 로드
df = pd.read_csv("../lsbigdata-project1/data/houseprice-with-lonlat.csv")
ames_df = df[["Longitude", "Latitude"]]

# 지도 객체 생성
map_sig = folium.Map(location=[42.034722, -93.62], zoom_start=12)

# MarkerCluster 추가
marker_cluster = MarkerCluster().add_to(map_sig)

# 마커 추가
for i in range(len(ames_df)):
    folium.Marker(
        location = [ames_df.iloc[i,1], ames_df.iloc[i,0]],
        popup = "houses"
    ).add_to(marker_cluster)

# 지도 저장
map_sig.save('maps/ames_MarkerCluster.html')
-------------------------------
# 방법 3
# 데이터 로드
df = pd.read_csv("../lsbigdata-project1/data/houseprice-with-lonlat.csv")

# 지도 객체 생성
map_sig = folium.Map(location=[42.034722, -93.62],
                     zoom_start=12,
                     tiles='cartodbpositron')
                     
# 마커 추가
for i in range(len(df)):
    x_point = df[["Latitude"]].iloc[i,0]
    x_float = float(x_point)
    y_point = df[["Longitude"]].iloc[i,0]
    y_float = float(y_point)
    folium.Marker([x_float, y_float]).add_to(map_sig)
    
# 지도 저장
map_sig.save('maps/ames_Marker(for-in).html')
-------------------------------
# 방법 4
CircleMarker 방법

import pandas as pd
import folium

# 데이터 로드
df = pd.read_csv("../lsbigdata-project1/data/houseprice-with-lonlat.csv")
Longitude = df['Longitude']
Latitude = df['Latitude']
Price = df['Sale_Price']

# 지도 객체 생성
map_sig = folium.Map(location=[42.034722, -93.62],
                     zoom_start=12,
                     tiles='cartodbpositron')
# 마커 추가
for i in range(len(df)):
    folium.CircleMarker([Latitude[i], Longitude[i]],
    popup = f"Price: ${Price[i]}",
    radius = 3,
    color = 'skyblue',
    fill_color = 'skyblue',
    fill = True,
    fill_opacity = 0.6).add_to(map_sig)

# 지도 저장
map_sig.save('maps/ames_CircleMarker.html')
----------------------------
import pandas as pd
import folium
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 데이터 로드
df = pd.read_csv("../lsbigdata-project1/data/houseprice-with-lonlat.csv")
Longitude = df['Longitude']
Latitude = df['Latitude']
Price = df['Sale_Price']
Neighborhood = df['Neighborhood']

# 지도 객체 생성
map_sig = folium.Map(location=[42.034722, -93.62],
                     zoom_start=12,
                     tiles='cartodbpositron')

# 고유한 Neighborhood 값을 추출하고, 이를 색상으로 매핑
neighborhoods = df['Neighborhood'].unique()
num_neighborhoods = len(neighborhoods)
colormap = plt.cm.get_cmap('tab10', num_neighborhoods)  # 동네 수에 맞춰 색상 설정
colors = {neighborhood: mcolors.rgb2hex(colormap(i)[:3]) for i, neighborhood in enumerate(neighborhoods)}

# 각 마커 추가
for i in range(len(df)):
    neighborhood_color = colors[Neighborhood[i]]
    popup_text = f"Neighborhood: {Neighborhood[i]}<br>Price: ${Price[i]:,.0f}"
    folium.CircleMarker(
        [Latitude[i], Longitude[i]],
        popup=popup_text,
        radius=3,
        color=neighborhood_color,
        fill_color=neighborhood_color,
        fill=True,
        fill_opacity=0.6
    ).add_to(map_sig)

# 주요 시설들의 위도, 경도, 이름 및 마커 정보
facilities = [
    {"name": "Mary Greeley Medical Center (병원)", "lat": 42.025, "lon": -93.615, "color": "red", "icon": "plus-sign"},
    {"name": "Ames High School (학교)", "lat": 42.029, "lon": -93.637, "color": "green", "icon": "education"},
    {"name": "Walmart Supercenter (마트)", "lat": 42.020, "lon": -93.609, "color": "blue", "icon": "shopping-cart"},
    {"name": "Ames Police Department (경찰서)", "lat": 42.026, "lon": -93.617, "color": "black", "icon": "info-sign"},
    {"name": "Ames Fire Department (소방서)", "lat": 42.022, "lon": -93.611, "color": "orange", "icon": "fire"},
]

# 마커 추가
for facility in facilities:
    folium.Marker(
        location=[facility["lat"], facility["lon"]],
        popup=facility["name"],
        icon=folium.Icon(color=facility["color"], icon=facility["icon"])
    ).add_to(map_sig)

# 지도 출력
map_sig.save('house_price_map.html')
