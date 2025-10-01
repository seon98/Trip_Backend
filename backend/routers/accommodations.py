# routers/accommodations.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# 다른 폴더에 있는 파일들을 가져오기 위해 ..을 사용합니다.
from .. import crud, schemas
from ..database import SessionLocal
from ..routers.auth import get_current_user  # 인증을 위한 의존성을 가져옵니다.

# APIRouter 인스턴스를 생성합니다.
router = APIRouter(
    prefix="/accommodations",
    tags=["accommodations"],
)


# --- 의존성 (Dependency) ---
# 각 API 요청마다 데이터베이스 세션을 생성하고 완료되면 닫습니다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- API 엔드포인트 ---


# CREATE: 새로운 숙소 생성 (로그인 필요)
@router.post("/", response_model=schemas.Accommodation)
def create_accommodation(
    accommodation: schemas.AccommodationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(
        get_current_user
    ),  # 👈 로그인한 사용자만 접근 가능
):
    """
    새로운 숙소 정보를 생성합니다.

    - **accommodation**: 이름, 위치, 가격 등이 포함된 숙소 정보.
    - **반환**: 생성된 숙소 정보 (DB에 저장된 id 포함).
    """
    return crud.create_accommodation(db=db, accommodation=accommodation)


# READ (All): 모든 숙소 목록 조회 (로그인 불필요)
@router.get("/", response_model=List[schemas.Accommodation])
def read_accommodations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    등록된 모든 숙소 목록을 조회합니다.

    - **skip**: 건너뛸 데이터 개수 (페이지네이션).
    - **limit**: 가져올 데이터 최대 개수 (페이지네이션).
    - **반환**: 숙소 정보 리스트.
    """
    accommodations = crud.get_accommodations(db, skip=skip, limit=limit)
    return accommodations


# READ (One): 특정 ID의 숙소 조회 (로그인 불필요)
@router.get("/{accommodation_id}", response_model=schemas.Accommodation)
def read_accommodation(accommodation_id: int, db: Session = Depends(get_db)):
    """
    특정 ID를 가진 숙소 하나의 정보를 조회합니다.

    - **accommodation_id**: 조회할 숙소의 고유 ID.
    - **반환**: 해당 ID의 숙소 정보.
    """
    db_accommodation = crud.get_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation


# UPDATE: 특정 숙소 정보 수정 (로그인 필요)
@router.put("/{accommodation_id}", response_model=schemas.Accommodation)
def update_accommodation(
    accommodation_id: int,
    accommodation: schemas.AccommodationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(
        get_current_user
    ),  # 👈 로그인한 사용자만 접근 가능
):
    """
    특정 ID를 가진 숙소의 정보를 수정합니다.

    - **accommodation_id**: 수정할 숙소의 고유 ID.
    - **accommodation**: 업데이트할 숙소 정보.
    - **반환**: 수정이 완료된 숙소 정보.
    """
    db_accommodation = crud.update_accommodation(
        db, accommodation_id=accommodation_id, accommodation_update=accommodation
    )
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation


# DELETE: 특정 숙소 정보 삭제 (로그인 필요)
@router.delete("/{accommodation_id}", response_model=schemas.Accommodation)
def delete_accommodation(
    accommodation_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(
        get_current_user
    ),  # 👈 로그인한 사용자만 접근 가능
):
    """
    특정 ID를 가진 숙소의 정보를 삭제합니다.

    - **accommodation_id**: 삭제할 숙소의 고유 ID.
    - **반환**: 삭제된 숙소의 정보.
    """
    db_accommodation = crud.delete_accommodation(db, accommodation_id=accommodation_id)
    if db_accommodation is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return db_accommodation
