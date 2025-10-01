# backend/crud.py

from typing import Optional  # 👈 Optional 타입을 가져옵니다.

from sqlalchemy.orm import Session, joinedload

from . import models, schemas, security

# --- Accommodation CRUD ---


def get_accommodation(db: Session, accommodation_id: int):
    return (
        db.query(models.Accommodation)
        .options(joinedload(models.Accommodation.owner))
        .filter(models.Accommodation.id == accommodation_id)
        .first()
    )


# ✨ get_accommodations 함수를 수정합니다.
def get_accommodations(
    db: Session, location: Optional[str] = None, skip: int = 0, limit: int = 100
):
    # 기본 쿼리를 먼저 만듭니다.
    query = db.query(models.Accommodation).options(
        joinedload(models.Accommodation.owner)
    )

    # 만약 location 파라미터가 주어졌다면, 필터 조건을 추가합니다.
    if location:
        # location 컬럼에 파라미터 값이 포함된(contains) 모든 숙소를 찾습니다.
        query = query.filter(models.Accommodation.location.contains(location))

    # 최종적으로 skip과 limit을 적용하여 결과를 반환합니다.
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


# --- Flight CRUD --- (변경 없음)
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


# --- User CRUD --- (변경 없음)
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
