# backend/routers/accommodations.py

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas, security  # 👈 security를 임포트합니다.
from ..database import get_db

# ❌ from ..routers.auth import get_current_user # 👈 이 줄을 삭제합니다.

router = APIRouter(
    prefix="/api/accommodations",
    tags=["accommodations"],
)

# --- API 엔드포인트 ---


@router.post("/", response_model=schemas.Accommodation)
def create_accommodation(
    accommodation: schemas.AccommodationCreate,
    db: Session = Depends(get_db),
    # ✨ Depends(get_current_user)를 Depends(security.get_current_active_user)로 수정
    current_user: models.User = Depends(security.get_current_active_user),
):
    return crud.create_accommodation(
        db=db, accommodation=accommodation, user_id=current_user.id
    )


@router.get("/", response_model=List[schemas.Accommodation])
def read_accommodations(
    location: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    accommodations = crud.get_accommodations(
        db, location=location, skip=skip, limit=limit
    )
    return accommodations


@router.get("/{accommodation_id}", response_model=schemas.Accommodation)
def read_accommodation(accommodation_id: int, db: Session = Depends(get_db)):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation


@router.put("/{accommodation_id}", response_model=schemas.Accommodation)
def update_accommodation(
    accommodation_id: int,
    accommodation: schemas.AccommodationCreate,
    db: Session = Depends(get_db),
    # ✨ Depends(get_current_user)를 Depends(security.get_current_active_user)로 수정
    current_user: models.User = Depends(security.get_current_active_user),
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


@router.delete("/{accommodation_id}", response_model=schemas.Accommodation)
def delete_accommodation(
    accommodation_id: int,
    db: Session = Depends(get_db),
    # ✨ Depends(get_current_user)를 Depends(security.get_current_active_user)로 수정
    current_user: models.User = Depends(security.get_current_active_user),
):
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    if db_accommodation.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="삭제할 권한이 없습니다."
        )
    return crud.delete_accommodation(db, accommodation_id=accommodation_id)
