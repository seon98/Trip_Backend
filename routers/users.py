from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db  # 👈 중앙화된 get_db를 가져옵니다.

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

# ❌ 여기에 있던 def get_db(): ... 함수를 삭제합니다.


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    return crud.create_user(db=db, user=user)
