# backend/schemas.py (전체 수정 코드)

from datetime import date
from typing import ForwardRef, List

from pydantic import BaseModel, ConfigDict

# --- Forward References ---
# 순환 참조를 해결하기 위해 ForwardRef를 사용합니다.
User = ForwardRef("User")
Accommodation = ForwardRef("Accommodation")
Flight = ForwardRef("Flight")
AccommodationBooking = ForwardRef("AccommodationBooking")
FlightBooking = ForwardRef("FlightBooking")

# --- Base Schemas first ---


class UserBase(BaseModel):
    email: str


class AccommodationBase(BaseModel):
    name: str
    location: str
    price: int
    description: str | None = None


class FlightBase(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str
    price: int


class AccommodationBookingBase(BaseModel):
    start_date: date
    end_date: date


class FlightBookingBase(BaseModel):
    booking_date: date


# --- Create Schemas ---


class UserCreate(UserBase):
    password: str


class AccommodationCreate(AccommodationBase):
    pass


class FlightCreate(FlightBase):
    pass


class AccommodationBookingCreate(AccommodationBookingBase):
    pass


class FlightBookingCreate(FlightBookingBase):
    pass


# --- Main Schemas for Reading Data ---


class UserInAccommodation(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)


class AccommodationInUser(BaseModel):
    id: int
    name: str
    location: str
    price: int
    model_config = ConfigDict(from_attributes=True)


class AccommodationBooking(AccommodationBookingBase):
    id: int
    status: str
    user_id: int
    accommodation_id: int
    model_config = ConfigDict(from_attributes=True)


class FlightBooking(FlightBookingBase):
    id: int
    status: str
    user_id: int
    flight_id: int
    model_config = ConfigDict(from_attributes=True)


class Accommodation(AccommodationBase):
    id: int
    owner_id: int
    owner: UserInAccommodation
    bookings: List[AccommodationBooking] = []
    model_config = ConfigDict(from_attributes=True)


class Flight(FlightBase):
    id: int
    bookings: List[FlightBooking] = []
    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id
