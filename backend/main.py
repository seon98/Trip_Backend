# backend/main.py (전체 코드 - 수정본)

from fastapi import FastAPI

# CORSMiddleware를 가져옵니다.
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import accommodations, auth, flights, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 허용할 출처(origin) 목록
origins = [
    "http://localhost:5173",  # 로컬 React 개발 서버 주소
    # "https://your-frontend-domain.com", # 나중에 프론트엔드를 배포할 경우 주소 추가
]

# CORS 미들웨어를 추가합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 출처 목록
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

app.include_router(accommodations.router)
app.include_router(flights.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "떠나봄 API 서버에 오신 것을 환영합니다!"}
