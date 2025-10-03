# backend/routers/bookings.py (전체 수정 코드)

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel  # 👈 여기에 누락되었던 import를 추가했습니다!
from sqlalchemy.orm import Session

from .. import crud, models, schemas, security
from ..database import get_db

router = APIRouter(
    prefix="/api/bookings",
    tags=["bookings"],
)


# --- 사용자 기능: 숙소 예약 생성 ---
@router.post(
    "/accommodations/{accommodation_id}", response_model=schemas.AccommodationBooking
)
def book_accommodation(
    accommodation_id: int,
    booking: schemas.AccommodationBookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="해당 숙소를 찾을 수 없습니다.")

    return crud.create_accommodation_booking(
        db=db,
        booking=booking,
        accommodation_id=accommodation_id,
        user_id=current_user.id,
    )


# --- 사용자 기능: 항공권 예약 생성 ---
@router.post("/flights/{flight_id}", response_model=schemas.FlightBooking)
def book_flight(
    flight_id: int,
    booking: schemas.FlightBookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    db_flight = crud.get_flight(db, flight_id=flight_id)
    if db_flight is None:
        raise HTTPException(status_code=404, detail="해당 항공권을 찾을 수 없습니다.")

    return crud.create_flight_booking(
        db=db, booking=booking, flight_id=flight_id, user_id=current_user.id
    )


# --- 사용자 기능: 내 예약 목록 조회 ---
class MyBookings(BaseModel):
    accommodations: List[schemas.AccommodationBooking]
    flights: List[schemas.FlightBooking]


@router.get("/my-bookings", response_model=MyBookings)
def read_my_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user),
):
    accommodation_bookings = crud.get_user_accommodation_bookings(
        db, user_id=current_user.id
    )
    flight_bookings = crud.get_user_flight_bookings(db, user_id=current_user.id)
    return {"accommodations": accommodation_bookings, "flights": flight_bookings}
