# main.py

from fastapi import FastAPI

from .database import Base, engine
from .routers import accommodations, auth, flights, users  # ✨ auth 라우터 추가 ✨

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1. 숙소 라우터를 메인 앱에 포함시킵니다.
app.include_router(accommodations.router)  # ✨ accommodations 라우터 포함 ✨
app.include_router(flights.router)  # ✨ flights 라우터 포함 ✨
app.include_router(users.router)  # ✨ users 라우터 포함 ✨
app.include_router(auth.router)  # ✨ auth 라우터 포함 ✨


# 2. (선택) 루트 경로와 같은 공통 API는 main.py에 남겨둘 수 있습니다.
@app.get("/")
def read_root():
    return {"message": "떠나봄 API 서버에 오신 것을 환영합니다!"}


@app.get("/")
def read_root():
    return {"message": "떠나봄 API 서버에 오신 것을 환영합니다!"}
