from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_accommodations_db = []


class Accommodation(BaseModel):
    name: str  # 숙소 이름 (문자열)
    location: str  # 위치 (문자열)
    price: int  # 가격 (정수)
    description: str | None = None  # 설명 (선택적 필드, 없어도 됨)


# --API 엔드포인트 구현--
@app.get("/")
async def read_root():
    return {"message": "안녕하세요, 떠나봄에 오신 것을 환영합니다!"}


@app.get("/accommodations/", response_model=List[Accommodation])
async def get_accommodations():
    return fake_accommodations_db


@app.post("/accommodations/", response_model=Accommodation)
async def create_accommodation(item: Accommodation):
    fake_accommodations_db.append(item)
    return item
