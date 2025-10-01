# routers/auth.py (새 파일)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, models, schemas, security
from ..database import SessionLocal

router = APIRouter(tags=["auth"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # 1. 사용자 이메일(form_data.username)로 DB에서 사용자 정보를 가져옵니다.
    user = crud.get_user_by_email(db, email=form_data.username)

    # 2. 사용자가 없거나 비밀번호가 틀리면 에러를 발생시킵니다.
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 잘못되었습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. 비밀번호가 맞다면, JWT 토큰을 생성합니다.
    access_token = security.create_access_token(data={"sub": user.email})

    # 4. 표준 형식에 맞춰 토큰을 반환합니다.
    return {"access_token": access_token, "token_type": "bearer"}


# ✨ --- 현재 로그인된 사용자를 가져오는 의존성 함수 --- ✨
def get_current_user(
    token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 1. 토큰을 검증하고 사용자 이메일을 가져옵니다.
    email = security.verify_token(token, credentials_exception)
    # 2. 이메일을 사용해 DB에서 사용자 정보를 조회합니다.
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    # 3. 사용자 정보를 반환합니다.
    return user
