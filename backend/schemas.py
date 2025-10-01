# schemas.py

from pydantic import BaseModel, ConfigDict


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
    model_config = ConfigDict(from_attributes=True)


# 항공권 스키마 추가
# 기본 항공권 정보
class FlightBase(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str
    price: int


# 항공권 생성 시 사용할 스키마
class FlightCreate(FlightBase):
    pass


# DB에서 읽어올 때 사용할 스키마 (id 포함)
class Flight(FlightBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ✨ --- User 스키마 추가 --- ✨
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str  # 생성 시에는 평문 비밀번호를 받음


class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
