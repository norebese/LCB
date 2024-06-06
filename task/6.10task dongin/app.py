import streamlit as st
from pymongo import MongoClient

url = 'mongodb+srv://c01039520824:VJlhIYbNW68HgIXu@cluster0.beqs9le.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(url)

database = client['aiproject'] # 데이터베이스 선택
collection = database['bookinfo'] # 컬렉션 선택

book_data = list(collection.find({}))

st.title('Book List')

# 페이지네이션 설정
page_size = 10  # 한 페이지에 보여줄 책의 개수
total_books = len(book_data)
total_pages = (total_books // page_size) + (1 if total_books % page_size > 0 else 0)  # 총 페이지 수 계산

# 사용자가 선택할 페이지 번호
page_number = st.selectbox('페이지 선택', range(1, total_pages + 1), index=0)

# 선택된 페이지의 데이터 가져오기
start_idx = (page_number - 1) * page_size
end_idx = min(start_idx + page_size, total_books)
display_books = book_data[start_idx:end_idx]

# 책 데이터를 2열로 배치하기 위해 컬럼 생성
row1, row2 = st.columns(2)

for book in display_books:
    col1, col2 = st.columns([1, 2])  # 첫 번째 컬럼은 표지 이미지, 두 번째 컬럼은 설명

    with col1:
        st.image(book['book_thumbnail'], width=150, use_column_width='auto')

    with col2:
        st.markdown(f"**책 이름 :**   {book['book_name']}")
        st.markdown(f"**카테고리 :**   {book['book_category']}")
        st.markdown(f"**저자 :**   {', '.join(book['book_author'])}")
        st.markdown(f"**출판사 :**   {book['book_publisher']}")
        st.markdown(f"**출간일 :**   {book['book_date']}")
        st.markdown(f"**가격 :**   {book['book_price']} 원")

# streamlit run app.py