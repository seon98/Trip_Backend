# crud.py

from sqlalchemy.orm import Session

from . import models, schemas


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
