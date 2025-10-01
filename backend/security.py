from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # 👈 OAuth2PasswordBearer 임포트 추가
from jose import JWTError, jwt
from passlib.context import CryptContext

# 사용하는 알고리즘을 "argon2"로 변경합니다. 이 한 줄이 핵심입니다.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# 아래 함수들은 변경할 필요가 전혀 없습니다.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# ✨ --- JWT 관련 코드를 추가 --- ✨

# ⚠️ 매우 중요: 이 SECRET_KEY는 외부에 노출되면 안 됩니다.
# 실제 운영 환경에서는 환경 변수 등을 통해 관리해야 합니다.
SECRET_KEY = (
    "c1a9b5f8d3e2c7a6b0f9d4e3c2a1b0f8"  # 예시 키입니다. 실제로는 더 복잡해야 합니다.
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 토큰 유효 기간 30분


def create_access_token(data: dict):
    to_encode = data.copy()
    # 토큰 만료 시간 설정
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # JWT 토큰 생성
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ✨ --- 토큰을 해독하고 유효한지 검사하는 함수 추가 --- ✨

# "/token" 엔드포인트로부터 토큰을 받아오는 객체 생성
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str, credentials_exception):
    try:
        # 토큰을 해독하여 payload(내용물)를 얻습니다.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email  # 이메일(사용자 아이디)을 반환
    except JWTError:
        raise credentials_exception
