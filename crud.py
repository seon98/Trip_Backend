from typing import Optional

from sqlalchemy.orm import Session, joinedload

import models
import schemas
import security


# --- Accommodation CRUD ---
def get_accommodation(db: Session, accommodation_id: int):
    return (
        db.query(models.Accommodation)
        .options(joinedload(models.Accommodation.owner))
        .filter(models.Accommodation.id == accommodation_id)
        .first()
    )


def get_accommodations(
    db: Session, location: Optional[str] = None, skip: int = 0, limit: int = 100
):
    query = db.query(models.Accommodation).options(
        joinedload(models.Accommodation.owner)
    )
    if location:
        query = query.filter(models.Accommodation.location.contains(location))
    return query.offset(skip).limit(limit).all()


def create_accommodation(
    db: Session, accommodation: schemas.AccommodationCreate, user_id: int
):
    db_accommodation = models.Accommodation(**accommodation.dict(), owner_id=user_id)
    db.add(db_accommodation)
    db.commit()
    db.refresh(db_accommodation)
    return db_accommodation


def update_accommodation(
    db: Session,
    accommodation_id: int,
    accommodation_update: schemas.AccommodationCreate,
):
    db_accommodation = get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation:
        update_data = accommodation_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_accommodation, key, value)
        db.commit()
        db.refresh(db_accommodation)
    return db_accommodation


def delete_accommodation(db: Session, accommodation_id: int):
    db_accommodation = get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation:
        db.delete(db_accommodation)
        db.commit()
    return db_accommodation


# --- Flight CRUD ---
def get_flight(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()


def get_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()


def create_flight(db: Session, flight: schemas.FlightCreate):
    db_flight = models.Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


# --- User CRUD ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# ✨ 관리자 기능을 위해 모든 사용자를 조회하는 함수 추가
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# --- Accommodation Booking CRUD ---
def create_accommodation_booking(
    db: Session,
    booking: schemas.AccommodationBookingCreate,
    accommodation_id: int,
    user_id: int,
):
    db_booking = models.AccommodationBooking(
        **booking.dict(), accommodation_id=accommodation_id, user_id=user_id
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_user_accommodation_bookings(db: Session, user_id: int):
    return (
        db.query(models.AccommodationBooking)
        .filter(models.AccommodationBooking.user_id == user_id)
        .all()
    )


# ✨ 관리자 기능을 위해 모든 숙소 예약을 조회하는 함수 추가
def get_all_accommodation_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AccommodationBooking).offset(skip).limit(limit).all()


# --- Flight Booking CRUD ---
def create_flight_booking(
    db: Session, booking: schemas.FlightBookingCreate, flight_id: int, user_id: int
):
    db_booking = models.FlightBooking(
        **booking.dict(), flight_id=flight_id, user_id=user_id
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_user_flight_bookings(db: Session, user_id: int):
    return (
        db.query(models.FlightBooking)
        .filter(models.FlightBooking.user_id == user_id)
        .all()
    )
