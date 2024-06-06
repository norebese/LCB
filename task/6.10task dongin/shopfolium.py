import folium as fm
import pandas as pd
from pymongo import MongoClient
import warnings
warnings.filterwarnings('ignore')

url = 'mongodb+srv://c01039520824:VJlhIYbNW68HgIXu@cluster0.beqs9le.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(url)

database = client['aiproject'] # 데이터베이스 선택
collection = database['shopinfo'] # 컬렉션 선택

result = collection.find({}) # 데이터 조회
data_list = list(result) # pymongo.cursor.Cursor 객체에서 리스트 생성

shop_df = pd.json_normalize(data_list) # 데이터 프레임으로 변환

shop_df_map = shop_df[['shop_type', 'shop_name', 'shop_address', 'latitude', 'longitude']]

# 위도, 경도 -> float 변환
shop_df_map['latitude'] = shop_df_map['latitude'].astype(float)
shop_df_map['longitude'] = shop_df_map['longitude'].astype(float)

# print(shop_df_map.loc[(shop_df_map['latitude'] == 0) | (shop_df_map['longitude'] == 0)])

shop_df_map = shop_df_map.loc[(shop_df_map['latitude'] > 0) & (shop_df_map['longitude'] > 0)] #위경도 오류처리된 것 처리

# print(shop_df_map)

shop_map = fm.Map(location=[shop_df_map['latitude'].mean(), shop_df_map['longitude'].mean()], zoom_start=12)

for index, data in shop_df_map.iterrows():
  popup_str = '{} {} ,상세주소:{}'.format(data['shop_type'], data['shop_name'], data['shop_address'])
  popup = fm.Popup(popup_str, max_width=600)
  if data['shop_type'] == '매머드 익스프레스': # 커스텀 아이콘 추가
    icon_url  = 'https://mmthcoffee.com/img/sub/mam_logo02.png'
  else:
    icon_url  = '	https://mmthcoffee.com/img/sub/mam_logo01.png'

  fm.Marker(location=[data['latitude'], data['longitude']], popup=popup, icon=fm.CustomIcon(icon_url, icon_size=(50, 50))).add_to(shop_map)

# shop_map.save("shop_map.html")
shop_map.show_in_browser()