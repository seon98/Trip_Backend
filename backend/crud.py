# backend/crud.py

from sqlalchemy.orm import Session, joinedload  # 👈 joinedload를 새로 가져옵니다.

from . import models, schemas, security

# --- Accommodation CRUD ---


# ✨ get_accommodation 함수를 수정합니다.
def get_accommodation(db: Session, accommodation_id: int):
    # .options(joinedload(...))를 추가하여 owner 정보를 함께 로딩하도록 합니다.
    return (
        db.query(models.Accommodation)
        .options(joinedload(models.Accommodation.owner))
        .filter(models.Accommodation.id == accommodation_id)
        .first()
    )


def get_accommodations(db: Session, skip: int = 0, limit: int = 100):
    # 전체 목록을 가져올 때도 owner 정보를 함께 로딩하면 성능에 좋습니다.
    return (
        db.query(models.Accommodation)
        .options(joinedload(models.Accommodation.owner))
        .offset(skip)
        .limit(limit)
        .all()
    )


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
