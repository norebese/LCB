@echo off

:: 가상환경 생성 (존재하지 않을 경우)
if not exist "venv" (
    python -m venv venv
)

:: 가상환경 활성화
call .\venv\Scripts\activate

:: pip 업그레이드
python -m pip install --upgrade pip

:: requirements.txt 파일이 존재하는지 확인
if not exist "requirements.txt" (
    echo requirements.txt 파일이 없습니다.
) else (
    :: requirements.txt에 있는 패키지 설치
    pip install -r requirements.txt
)

:: pymongo[srv] 패키지 설치
python -m pip install "pymongo[srv]==3.11"

:: Visual Studio Code 설정 디렉토리 생성
if not exist ".vscode" (
    mkdir .vscode
)

:: Visual Studio Code 설정 파일 생성 및 가상환경 설정 추가
echo {
echo     "python.pythonPath": "%cd%\venv\Scripts\python.exe",
echo     "python.terminal.activateEnvironment": true
echo } > .vscode\settings.json

:: Visual Studio Code 실행
code .

:: 명령 프롬프트 창 유지
cmd /k