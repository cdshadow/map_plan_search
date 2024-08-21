import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import GoogleV3
import geopandas as gpd

# Google Geocoding API 키 설정
api_key = "AIzaSyCW-4kxARbJUxL3jmOz5dR5D-AabKhDJdc"  # 여기에 당신의 Google API 키를 입력하세요.

# Streamlit 설정
st.set_page_config(layout="wide")

# 데이터 파일 경로
shp_file_path_1f = 'https://raw.githubusercontent.com/cdshadow/map_plan/main/1f_2.shp'
shp_file_path_3f = 'https://raw.githubusercontent.com/cdshadow/map_plan/main/3f_2.shp'

# Geopy를 사용하여 입력된 위치의 좌표를 가져오기
geolocator = GoogleV3(api_key=api_key)

# 사용자 위치 입력
st.sidebar.title("현위치 입력")
location_input = st.sidebar.text_input("위치 입력 (예: 서울, 대전, New York)", "대전")

# 입력된 위치의 좌표를 가져오기
location = geolocator.geocode(location_input)

# Folium 지도 생성 함수
def create_map(center_location=[36.3504, 127.3845]):
    # Folium 지도 설정 (대전광역시 또는 사용자가 입력한 위치 중심)
    map_obj = folium.Map(
        location=center_location,  # 중심 좌표 설정
        zoom_start=12,  # 줌 레벨 조정
    )

    # 1f.shp 파일 불러오기
    gdf_1f = gpd.read_file(shp_file_path_1f)

    # EPSG 5179에서 EPSG 4326으로 좌표계 변환
    gdf_1f = gdf_1f.to_crs(epsg=4326)

    # 1f 레이어 추가 (검정색 선, 두께 0.5)
    folium.GeoJson(
        gdf_1f,
        name='1f 레이어',
        style_function=lambda feature: {
            'color': 'red',
            'weight': 0.5,
        }
    ).add_to(map_obj)

    # 3f.shp 파일 불러오기
    gdf_3f = gpd.read_file(shp_file_path_3f)

    # EPSG 5179에서 EPSG 4326으로 좌표계 변환
    gdf_3f = gdf_3f.to_crs(epsg=4326)

    # 3f 레이어 추가 (검정색 선, 두께 0.5)
    folium.GeoJson(
        gdf_3f,
        name='3f 레이어',
        style_function=lambda feature: {
            'color': 'red',
            'weight': 0.5,
        }
    ).add_to(map_obj)

    # 레이어 컨트롤 추가
    folium.LayerControl(position='topleft').add_to(map_obj)

    return map_obj

# 지도를 생성하고, 사용자가 입력한 위치를 기반으로 중심 이동
if location:
    map_display = create_map(center_location=[location.latitude, location.longitude])
    folium.Marker([location.latitude, location.longitude], tooltip="Current Location").add_to(map_display)
else:
    st.error("위치를 찾을 수 없습니다. 다시 입력해 주세요.")
    map_display = create_map()

# 지도 출력
st_folium(map_display, width=1200, height=700)
