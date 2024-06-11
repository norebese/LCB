# 가상환경 생성 (존재하지 않을 경우)
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 가상환경 활성화
source venv/bin/activate

# pip 업그레이드
python3 -m pip install --upgrade pip

# requirements.txt 파일이 존재하는지 확인
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt 파일이 없습니다."
else
    # requirements.txt에 있는 패키지 설치
    pip install -r requirements.txt
fi

# pymongo[srv] 패키지 설치
pip install "pymongo[srv]==3.11"

# Visual Studio Code 설정 디렉토리 생성
mkdir -p .vscode

# Visual Studio Code 설정 파일 생성 및 가상환경 설정 추가
cat <<EOL > .vscode/settings.json
{
    "python.pythonPath": "\${workspaceFolder}/`venv/bin/python",
    "python.terminal.activateEnvironment": true
}
EOL

# Visual Studio Code 실행
code .

# Visual Studio Code 실행
code .

# 쉘 유지
exec "$SHELL"
