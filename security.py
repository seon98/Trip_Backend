# backend/security.py (전체 수정 코드)

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import crud
import models
from database import get_db

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# oauth2_scheme은 여기서 정의되어야 합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception


# --- 웹 페이지(쿠키 기반)용 인증 함수 ---
def get_current_user_from_cookie(
        request: Request, db: Session = Depends(get_db)
) -> Optional[models.User]:
    token = request.cookies.get("access_token")
    if not token:
        return None

    if token.startswith("Bearer "):
        token = token.split("Bearer ")[1]

    try:
        email = verify_token(
            token, credentials_exception=HTTPException(status_code=401)
        )
        user = crud.get_user_by_email(db, email=email)
        return user
    except HTTPException:
        return None


# --- API(헤더 기반)용 인증 함수 ---
def get_current_active_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_token(token, credentials_exception)
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


# --- 쿠키 기반 관리자 확인 함수 ---
def get_current_admin_user_from_cookie(
        current_user: models.User = Depends(get_current_user_from_cookie),
) -> models.User:
    if not current_user or current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 없습니다."
        )
    return current_user


# --- API 기반 관리자 확인 함수 ---
def get_current_admin_user(
        current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 없습니다."
        )
    return current_user
