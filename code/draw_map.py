# 本项目旨在通过获取"GPS记录器app"的定位数据绘制用户的路线图
# 首先需要将GPS记录器的定位数据上传到data文件夹下，文件格式为geojson
# 全局科学上网能加速加载线路图
# pip install folium
import json
import datetime

import folium
from folium import PolyLine

## 初始化配置
data_path = r'../data\nse-2720013373226014400-20230223.geojson.geojson' # 原始数据的存储路径
save_path = r'../map/20230223.html'                                     # 生成地图的存储路径
time_format = "%Y-%m-%d %H:%M:%S"                                       # 时间格式
_3D = False                                                             # 如果为True则返回3维卫星地图，否则为2维地图

## 加载原始数据
with open(data_path, 'r') as f:
    data = json.load(f).get('features')

def get_gps_info(sub_data):
    timestamp = datetime.datetime.fromisoformat(sub_data.get('properties').get('time')).strftime(time_format)
    geometry = sub_data.get('geometry').get('coordinates')
    longitude, latitude = geometry
    return [timestamp, latitude, longitude]

gps_info = list(map(get_gps_info, data))

## 地图初始化
map = folium.Map(location=gps_info[0][-2:], zoom_start=15)
if _3D:
    folium.TileLayer(
        tiles="https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
        attr="Google",
        name="Google Satellite",
        overlay=True,
        control=True,
    ).add_to(map)

## 在地图上添加点以及绘制线路图
for sub_data in gps_info:
    marker = folium.Marker(location=[sub_data[1], sub_data[2]], tooltip=sub_data[0], popup=f'<div style="width:150px;height:45px;">时间: {sub_data[0]}<br>纬度: {sub_data[1]}<br>经度: {sub_data[2]}</div>')
    marker.add_to(map)

route = PolyLine(
    locations=[sub_data[-2:] for sub_data in gps_info],
    text="行车路线",
    offset=10,
    color="blue",
    weight=5,
    opacity=0.7,
    dash_array=[10, 5]
)
route.add_to(map)
map.save(save_path)
