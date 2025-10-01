# backend/routers/accommodations.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status  # status 임포트 추가
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


# READ (All) (변경 없음)
@router.get("/", response_model=List[schemas.Accommodation])
def read_accommodations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accommodations = crud.get_accommodations(db, skip=skip, limit=limit)
    return accommodations


# READ (One) (변경 없음)
@router.get("/{accommodation_id}", response_model=schemas.Accommodation)
def read_accommodation(accommodation_id: int, db: Session = Depends(get_db)):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation


# UPDATE: 특정 숙소 정보 수정 (✨ 권한 확인 로직 추가)
@router.put("/{accommodation_id}", response_model=schemas.Accommodation)
def update_accommodation(
    accommodation_id: int,
    accommodation: schemas.AccommodationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    # 먼저 DB에서 해당 ID의 숙소를 가져옵니다.
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)

    # 숙소가 존재하지 않는 경우 404 에러
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")

    # ✨ 핵심: 숙소의 소유자 ID와 현재 로그인한 사용자의 ID가 다른 경우 403 에러
    if db_accommodation.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="수정할 권한이 없습니다."
        )

    # 모든 검사를 통과하면 수정 로직을 실행합니다.
    return crud.update_accommodation(
        db, accommodation_id=accommodation_id, accommodation_update=accommodation
    )


# DELETE: 특정 숙소 정보 삭제 (✨ 권한 확인 로직 추가)
@router.delete("/{accommodation_id}", response_model=schemas.Accommodation)
def delete_accommodation(
    accommodation_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    # 먼저 DB에서 해당 ID의 숙소를 가져옵니다.
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)

    # 숙소가 존재하지 않는 경우 404 에러
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")

    # ✨ 핵심: 숙소의 소유자 ID와 현재 로그인한 사용자의 ID가 다른 경우 403 에러
    if db_accommodation.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="삭제할 권한이 없습니다."
        )

    # 모든 검사를 통과하면 삭제 로직을 실행합니다.
    return crud.delete_accommodation(db, accommodation_id=accommodation_id)
