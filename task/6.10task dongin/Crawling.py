import requests
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient

mongo_url = 'mongodb+srv://c01039520824:VJlhIYbNW68HgIXu@cluster0.beqs9le.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(mongo_url) # 응답 확인
database = client['aiproject'] # 데이터베이스 선택
collection = database['bookinfo'] # 컬렉션 선택

search_keyword = '인공지능'

# URL에서 한글이나 특수문자 등을 사용할 때는 보통 URL 인코딩을 한다고 함
# urllib.parse.quote() 함수를 사용하여 검색어를 인코딩하여 저장한다
encoded_keyword = urllib.parse.quote(search_keyword, encoding='utf-8')

# url = f'https://search.kyobobook.co.kr/search?keyword={encoded_keyword}&target=total&gbCode=TOT&page=1'
# url = 'https://search.kyobobook.co.kr/search?keyword=%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5&target=total&gbCode=TOT&page=1'
# request = requests.get(url)
# print(request)

# soup = BeautifulSoup(request.text, "html.parser")
# # print(request.text)

# divs = soup.find('span', {'id': 'cmdtName_S000209182535'})
# print(divs)

#BeautifulSoup은 정적으로 HTML을 파싱하는 라이브러리이기 때문에, 초기에 로드된 HTML 소스만을 기반으로 작동합니다. 즉, 페이지가 JavaScript나 AJAX 등을 사용하여 동적으로 데이터를 로드하거나 업데이트할 경우, 초기에 로드된 HTML 소스에는 해당 동적으로 생성되는 요소들이 포함되어 있지 않을 수 있습니다. 이 경우 BeautifulSoup으로는 해당 동적 요소들을 가져오기 어렵습니다.

driver = webdriver.Chrome()
totalPage = 1
currentPage = 1
try:
    while currentPage <= totalPage:
        driver.get(f'https://search.kyobobook.co.kr/search?keyword={encoded_keyword}&target=total&gbCode=TOT&page={currentPage}')

        soup = BeautifulSoup(driver.page_source,  'html.parser')

        # 마지막 페이지 번호 가져옴
        totalPage = int(soup.find(class_="btn_page_num", attrs={"data-role": "last"}).text)
        
        book_list_area = soup.find_all('ul', {'class': 'prod_list'})

        # 각 링크에서 도서 정보 가져오기
        for books in book_list_area:
            book_info = books.find_all('div', {'class': 'prod_area horizontal'})
            for book in book_info:
                try:
                    alias = book.find('span', {'class': 'prod_alias'})
                    name = book.find('a', {'class': 'prod_info'}).find_all('span')[-1].text.strip()
                    book_name = f"{alias.text.strip()} {name}" if alias else name #조건부 표현식 사용
                    book_category = book.find('span', {'class': 'prod_category'}).text.strip()
                    book_thumbnail = book.find('span', {'class': 'img_box'}).find('img')['src']
                    book_author = [author.text.strip() for author in book.find_all('a', {'class': 'author'})] #리스트 컴프리헨션
                    book_publisher = book.find('div', {'class': 'prod_publish'}).find('a').text.strip()
                    book_date = book.find('span', {'class': 'date'}).text.strip()
                    book_price = book.find('span', {'class': 'price'}).find('span', {'class': 'val'}).text.strip()
                    # print(book_price)

                    #몽고디비에 삽입
                    data_insert = {'book_name': book_name, 'book_category': book_category,'book_thumbnail': book_thumbnail,'book_author': book_author,'book_publisher': book_publisher,'book_date': book_date,'book_price': book_price,}
                    result = collection.insert_one(data_insert) # 데이터 추가
                    print(f'입력된 데이터 id: {result.inserted_id}')
                
                except Exception as e:
                    print(f"크롤링 중 에러 발생: {e}")

            #close 추가

        currentPage+=1
        
finally:
    driver.quit()