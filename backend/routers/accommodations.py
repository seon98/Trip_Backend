# backend/routers/accommodations.py

from typing import List, Optional  # 👈 Optional 타입을 가져옵니다.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import SessionLocal
from ..routers.auth import get_current_user

router = APIRouter(
    prefix="/accommodations",
    tags=["accommodations"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API 엔드포인트 ---


# CREATE (변경 없음)
@router.post("/", response_model=schemas.Accommodation)
def create_accommodation(
    accommodation: schemas.AccommodationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.create_accommodation(
        db=db, accommodation=accommodation, user_id=current_user.id
    )


# ✨ READ (All): 모든 숙소 목록 조회 (location 쿼리 파라미터 추가)
@router.get("/", response_model=List[schemas.Accommodation])
def read_accommodations(
    location: Optional[str] = None,  # 👈 location 파라미터를 추가합니다.
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    등록된 모든 숙소 목록을 조회하거나, 특정 지역(location)으로 필터링합니다.

    - **location**: 검색할 지역 이름 (선택 사항).
    - **skip**: 건너뛸 데이터 개수 (페이지네이션).
    - **limit**: 가져올 데이터 최대 개수 (페이지네이션).
    """
    accommodations = crud.get_accommodations(
        db, location=location, skip=skip, limit=limit
    )
    return accommodations


# READ (One) (변경 없음)
@router.get("/{accommodation_id}", response_model=schemas.Accommodation)
def read_accommodation(accommodation_id: int, db: Session = Depends(get_db)):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation


# UPDATE (변경 없음)
@router.put("/{accommodation_id}", response_model=schemas.Accommodation)
def update_accommodation(
    accommodation_id: int,
    accommodation: schemas.AccommodationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    if db_accommodation.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="수정할 권한이 없습니다."
        )
    return crud.update_accommodation(
        db, accommodation_id=accommodation_id, accommodation_update=accommodation
    )


# DELETE (변경 없음)
@router.delete("/{accommodation_id}", response_model=schemas.Accommodation)
def delete_accommodation(
    accommodation_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    if db_accommodation.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="삭제할 권한이 없습니다."
        )
    return crud.delete_accommodation(db, accommodation_id=accommodation_id)
