# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 데이터베이스 접속 주소 설정
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db" # PostgreSQL 예시
SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./tteonabom.db"  # SQLite 사용, ./tteonabom.db 파일에 저장됨
)

# 2. 데이터베이스 엔진 생성
# connect_args는 SQLite 사용 시에만 필요한 설정입니다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 데이터베이스와 상호작용하기 위한 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. DB 모델을 만들기 위한 기본 클래스 생성
Base = declarative_base()
