# TASK Directory

## 1. 초기 설정 실행
1. 윈도우의 경우
  setup_window.bat 실행
2. 리눅스/맥의 경우
  setup_linux.sh 실행

## 2. 환경 작업
1. 현재 파이썬이 가상환경인지 확인하는 명령어
  ```cmd
  python -c "import sys; print(sys.prefix)"
  ```
2. 현재 파이썬 가상환경에 설치된 라이브러리들을 requirements로 만들기
  ```cmd
  pip freeze > requirements.txt
  ```