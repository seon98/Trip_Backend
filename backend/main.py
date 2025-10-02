from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import accommodations, auth, flights, users

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# -------------------- ✨ 수정된 부분 시작 ✨ --------------------

# 허용할 출처(origin) 목록을 더 관대하게 설정합니다.
origins = [
    "http://localhost",
    "http://localhost:5173",  # React 개발 서버의 기본 주소
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
    # "https://your-frontend-domain.com", # 나중에 프론트엔드를 배포할 경우 실제 도메인 주소 추가
]

# CORS 미들웨어를 추가합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 출처 목록
    allow_credentials=True,  # 쿠키를 포함한 요청 허용
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# -------------------- ✨ 수정된 부분 끝 ✨ --------------------


# 각 라우터를 앱에 포함시킵니다.
app.include_router(accommodations.router)
app.include_router(flights.router)
app.include_router(users.router)
app.include_router(auth.router)


# 루트 경로 API
@app.get("/")
def read_root():
    return {"message": "떠나봄 API 서버에 오신 것을 환영합니다!"}
