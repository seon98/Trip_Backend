# backend/routers/auth.py (전체 수정 코드)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, security
from ..database import get_db

router = APIRouter(
    prefix="/api",  # 👈 /token 앞에 /api를 붙이기 위해 prefix를 /api로 설정
    tags=["auth"],
)


# security.py의 tokenUrl도 수정해야 합니다.
# 우선 여기서 로그인 API를 정의합니다.
@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # ... (로그인 로직은 동일)
    pass
