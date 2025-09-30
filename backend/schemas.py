# schemas.py

from pydantic import BaseModel


# 기본 숙소 정보 스키마
class AccommodationBase(BaseModel):
    name: str
    location: str
    price: int
    description: str | None = None


# 숙소 생성 시 사용할 스키마
class AccommodationCreate(AccommodationBase):
    pass


# DB에서 읽어올 때 사용할 숙소 스키마 (id 포함)
class Accommodation(AccommodationBase):
    id: int

    # ORM 객체를 Pydantic 모델로 변환해주는 설정
    class Config:
        orm_mode = True
