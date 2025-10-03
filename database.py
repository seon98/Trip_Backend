from sqlalchemy import create_engine
from sqlalchemy.orm import (
	declarative_base,  # 👈 declarative_base 추가
	sessionmaker,
)

from config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ✨ 여기에 get_db 함수를 추가합니다.
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
