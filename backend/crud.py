# crud.py

from sqlalchemy.orm import Session

from . import models, schemas, security


# 특정 숙소 조회 (ID 기준)
def get_accommodation(db: Session, accommodation_id: int):
    return (
        db.query(models.Accommodation)
        .filter(models.Accommodation.id == accommodation_id)
        .first()
    )


# 전체 숙소 목록 조회
def get_accommodations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Accommodation).offset(skip).limit(limit).all()


# 숙소 생성
def create_accommodation(db: Session, accommodation: schemas.AccommodationCreate):
    # Pydantic 모델을 SQLAlchemy 모델 객체로 변환
    db_accommodation = models.Accommodation(**accommodation.dict())
    db.add(db_accommodation)  # DB 세션에 추가
    db.commit()  # DB에 변경사항 저장
    db.refresh(db_accommodation)  # 저장된 객체로 세션 새로고침 (ID 등)
    return db_accommodation


# 숙소 정보 수정 (Update)
def update_accommodation(
    db: Session,
    accommodation_id: int,
    accommodation_update: schemas.AccommodationCreate,
):
    # 1. ID를 기준으로 DB에서 수정할 데이터를 찾습니다.
    db_accommodation = get_accommodation(db, accommodation_id=accommodation_id)

    if db_accommodation:
        # 2. Pydantic 모델에서 받은 데이터(accommodation_update)를 딕셔너리로 변환합니다.
        update_data = accommodation_update.dict(exclude_unset=True)

        # 3. 딕셔너리의 각 키와 값을 기준으로 DB 모델 객체의 속성을 업데이트합니다.
        for key, value in update_data.items():
            setattr(db_accommodation, key, value)

        db.commit()  # 변경사항을 DB에 커밋(저장)합니다.
        db.refresh(db_accommodation)  # DB로부터 업데이트된 객체 정보를 새로고침합니다.

    return db_accommodation


# 숙소 정보 삭제 (Delete)
def delete_accommodation(db: Session, accommodation_id: int):
    db_accommodation = get_accommodation(db, accommodation_id=accommodation_id)

    if db_accommodation:
        db.delete(db_accommodation)  # 해당 객체를 DB 세션에서 삭제하도록 표시합니다.
        db.commit()  # 변경사항을 DB에 커밋합니다.

    return db_accommodation


# 항공권 CRUD 추가
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


# ✨ --- User CRUD 함수 추가 --- ✨
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    # 비밀번호를 해싱하여 저장
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
