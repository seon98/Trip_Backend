# routers/accommodations.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# ..은 상위 폴더를 의미합니다. 상위 폴더의 crud, models 등을 가져옵니다.
from .. import crud, models, schemas
from ..database import SessionLocal

# 1. APIRouter 인스턴스 생성
# prefix: 이 라우터의 모든 경로 앞에 /accommodations가 자동으로 붙습니다.
# tags: FastAPI 자동 문서에서 API들을 "accommodations" 그룹으로 묶어줍니다.
router = APIRouter(
    prefix="/accommodations",
    tags=["accommodations"],
)


# --- Dependency (main.py에서 가져옴) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 2. 경로 데코레이터를 @app에서 @router로 변경
# prefix 덕분에 URL 경로에서 /accommodations를 생략하고 "/" 만 사용합니다.
@router.post("/", response_model=schemas.Accommodation)
def create_accommodation(
    accommodation: schemas.AccommodationCreate, db: Session = Depends(get_db)
):
    return crud.create_accommodation(db=db, accommodation=accommodation)


@router.get("/", response_model=List[schemas.Accommodation])
def read_accommodations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accommodations = crud.get_accommodations(db, skip=skip, limit=limit)
    return accommodations


# 경로에서 "/{accommodation_id}" 부분만 남깁니다.
@router.get("/{accommodation_id}", response_model=schemas.Accommodation)
def read_accommodation(accommodation_id: int, db: Session = Depends(get_db)):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation


# PUT: 숙소 정보 수정
@router.put("/{accommodation_id}", response_model=schemas.Accommodation)
def update_accommodation(
    accommodation_id: int,
    accommodation: schemas.AccommodationCreate,
    db: Session = Depends(get_db),
):
    db_accommodation = crud.update_accommodation(
        db, accommodation_id=accommodation_id, accommodation_update=accommodation
    )
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation


# DELETE: 숙소 정보 삭제
@router.delete("/{accommodation_id}", response_model=schemas.Accommodation)
def delete_accommodation(accommodation_id: int, db: Session = Depends(get_db)):
    db_accommodation = crud.delete_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation
