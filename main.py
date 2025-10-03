# backend/main.py (전체 수정 코드)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 👇 Base와 engine을 임포트합니다
from database import Base, engine

# 👇 admin_pages 라우터를 새로 가져옵니다.
from routers import accommodations, admin, admin_pages, auth, bookings, flights, pages, users

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pages.router)
app.include_router(accommodations.router)
app.include_router(flights.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(admin.router)
app.include_router(admin_pages.router)  # 👈 새로운 admin_pages 라우터를 등록합니다.


@app.get("/api-root")
def read_api_root():
    return {"message": "API 서버 루트"}
