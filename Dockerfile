# Dockerfile

# 1. 베이스 이미지 선택 (Python 3.11의 가벼운 버전)
FROM python:3.11-slim

# 2. 컨테이너 안의 작업 디렉토리 설정
WORKDIR /app

# 3. .env 파일과 backend 폴더를 컨테이너 안으로 복사
COPY ./.env /app/.env
COPY ./backend /app/backend

# 4. requirements.txt 파일을 복사하고 uv를 이용해 라이브러리 설치
COPY ./requirements.txt /app/requirements.txt
RUN pip install uv

# 👇 이 명령어에 --system 옵션을 추가합니다.
RUN uv pip install --system --no-cache-dir -r requirements.txt

# 5. 컨테이너가 시작될 때 실행할 명령어
# --host 0.0.0.0는 컨테이너 외부에서 접속을 허용하기 위해 필수입니다.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
