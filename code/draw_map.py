# 本项目旨在通过获取"两步路"的定位数据绘制用户的路线图
# 首先需要将GPS记录器的定位数据上传到data文件夹下，文件格式为kml
# 全局科学上网能加速加载线路图
# pip install folium
from bs4 import BeautifulSoup
import re
from datetime import datetime
import folium
from folium import PolyLine


data_path = r'../data\nse-5442193384823581830-2023-02-23 2119西安长安区.kml.kml'
save_path = r'../map/20230224.html'                                             # 生成地图的存储路径
_3D = True                                                                     # 如果为True则返回3维卫星地图，否则为2维地图

with open(data_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'xml')
    track = soup.find('gx:Track')
    content = str(track)

pattern = re.compile(r'<gx:coord>(.*?)</gx:coord>', re.S)
locations = pattern.findall(content)
locations = [location.strip().split() for location in locations]    # 经度、纬度、海拔
locations = [list(map(float, location)) for location in locations]
pattern = re.compile(r'<when>(.*?)</when>', re.S)
timestamps = pattern.findall(content)
timestamps = [datetime.strptime(timestamp.strip(), '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S') for timestamp in timestamps]

## 地图初始化
map = folium.Map(location=locations[0][:2][::-1], zoom_start=15)
if _3D:
    folium.TileLayer(
        tiles="https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
        attr="Google",
        name="Google Satellite",
        overlay=True,
        control=True,
    ).add_to(map)

## 在地图上添加点以及绘制线路图
for idx in range(0, len(locations), 3):
    location = locations[idx]
    timestamp = timestamps[idx]
    marker = folium.Marker(location=[location[1], location[0]], tooltip=timestamp, popup=f'<div style="width:150px;height:55px;">时间: {timestamp}<br>纬度: {location[1]}<br>经度: {location[0]}<br>海拔: {location[2]}</div>')
    marker.add_to(map)

route = PolyLine(
    locations=[sub_data[:2][::-1] for sub_data in locations],
    text="路线",
    offset=10,
    color="blue",
    weight=5,
    opacity=0.7,
    dash_array=[10, 5]
)
route.add_to(map)
map.save(save_path)

# 1、浏览历史线路图，并按照时间进行筛选（连接数据库）
# 2、将照片添加到地图上
# 3、对比pyechars与folium两种实现方式的不同，寻找一种最佳实现方式
# 4、利用PyQt5构建一个GUI界面
# 5、如果要添加图片要考虑有效地压缩图片