# main.py

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# 방금 만든 파일들에서 필요한 것들을 가져옵니다.
from . import crud, models, schemas
from .database import SessionLocal, engine

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# --- Dependency ---
# API가 호출될 때마다 DB 세션을 생성하고, 끝나면 닫아주는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API Endpoints ---


# 숙소 생성
@app.post("/accommodations/", response_model=schemas.Accommodation)
def create_accommodation(
    accommodation: schemas.AccommodationCreate, db: Session = Depends(get_db)
):
    return crud.create_accommodation(db=db, accommodation=accommodation)


# 전체 숙소 목록 조회
@app.get("/accommodations/", response_model=List[schemas.Accommodation])
def read_accommodations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accommodations = crud.get_accommodations(db, skip=skip, limit=limit)
    return accommodations


# 특정 숙소 조회
@app.get("/accommodations/{accommodation_id}", response_model=schemas.Accommodation)
def read_accommodation(accommodation_id: int, db: Session = Depends(get_db)):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation
