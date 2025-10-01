# backend/schemas.py

from typing import List

from pydantic import BaseModel, ConfigDict

# --- Accommodation Schemas ---


class AccommodationBase(BaseModel):
    name: str
    location: str
    price: int
    description: str | None = None


class AccommodationCreate(AccommodationBase):
    pass


# User 정보를 표현하기 위한 스키마 (Accommodation 응답에 포함될 부분)
class UserInAccommodation(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)


class Accommodation(AccommodationBase):
    id: int
    owner_id: int
    # owner 필드를 추가하여 소유자 정보를 포함시킵니다.
    owner: UserInAccommodation
    model_config = ConfigDict(from_attributes=True)


# --- Flight Schemas ---


class FlightBase(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str
    price: int


class FlightCreate(FlightBase):
    pass


class Flight(FlightBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


# Accommodation 정보를 표현하기 위한 스키마 (User 응답에 포함될 부분)
class AccommodationInUser(BaseModel):
    id: int
    name: str
    location: str
    price: int
    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int
    # accommodations 필드를 추가하여 소유한 숙소 목록을 포함시킵니다.
    accommodations: List[AccommodationInUser] = []
    model_config = ConfigDict(from_attributes=True)
