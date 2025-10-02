# backend/main.py (전체 수정 코드 - 최종 테스트용)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import accommodations, auth, flights, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

# -------------------- ✨ 수정된 부분 시작 ✨ --------------------

# 모든 출처를 허용하도록 설정합니다. (디버깅 목적)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- ✨ 수정된 부분 끝 ✨ --------------------

app.include_router(accommodations.router)
app.include_router(flights.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "떠나봄 API 서버에 오신 것을 환영합니다!"}
