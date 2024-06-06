#1. 커피점 프렌차이즈 매장 또는 메뉴등을 크롤링하여, MongoDB에 데이터를 삽입 지도를 이용하여 표기
import requests, json
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from pymongo import MongoClient

mongo_url = 'mongodb+srv://c01039520824:VJlhIYbNW68HgIXu@cluster0.beqs9le.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(mongo_url) # 응답 확인
database = client['aiproject'] # 데이터베이스 선택
collection = database['shopinfo'] # 컬렉션 선택

url = 'https://mmthcoffee.com/sub/store.html'
request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

shop_list_area = soup.find('div', {'class': 'right'})

shop_list = shop_list_area.find_all('li')

def get_location(address): # 카카오 api 사용해서 주소로 위경도 구하는 함수
    try:
        only_address = address.split(',')[0]
        url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + only_address
        headers = {"Authorization": "KakaoAK 8b30caba0f98cca66d985e35af79f80d"}
        api_json = json.loads(str(requests.get(url,headers=headers).text))
        only_address = api_json['documents'][0]['address']
        crd = {"lat": str(only_address['y']), "lng": str(only_address['x'])}
        return crd
    except Exception as e:
        print(f"주소 변환중 에러 발생: {e}")
        return {"lat": '0', "lng": '0'}

for shop in shop_list:
    try:
        shop_type_symbol = shop.find('div', {'class': 'symbol'}).find('i').get('class')
        shop_type = '매머드 익스프레스' if 'e' in shop_type_symbol else '매머드커피'
        shop_name = shop.find('div', {'class': 'tit'}).find('strong').text
        shop_address = shop.find('div', {'class': 'txt'}).find('p').text.split(':')[1].strip()
        only_address = shop_address.split(',')[0]
        location = get_location(shop_address)
        # print(shop_type)

        data_insert = {'shop_type': shop_type, 'shop_name': shop_name, 'shop_address': shop_address,'latitude': location['lat'],'longitude': location['lng']}
        result = collection.insert_one(data_insert) # 데이터 추가
        print(f'입력된 데이터 id: {result.inserted_id}')
    except Exception as e:
        print(f"삽입중 에러 발생: {e}")