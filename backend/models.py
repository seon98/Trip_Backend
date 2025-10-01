# models.py

from sqlalchemy import Column, Integer, String

from .database import Base


# 'accommodations' 테이블을 나타내는 SQLAlchemy 모델
class Accommodation(Base):
    __tablename__ = "accommodations"

    id = Column(Integer, primary_key=True, index=True)  # 고유 ID, 기본 키
    name = Column(String, index=True)
    location = Column(String)
    price = Column(Integer)
    description = Column(String, nullable=True)  # Null 값을 허용

# 항공권 모델 추가
class Flight(Base):
    __tablename__ = "flights"  # 테이블 이름은 'flights'

    id = Column(Integer, primary_key=True, index=True)
    departure_airport = Column(String, index=True)
    arrival_airport = Column(String, index=True)
    departure_time = Column(String)
    arrival_time = Column(String)
    price = Column(Integer)

# ✨ --- User 모델 추가 --- ✨
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True) # 이메일을 아이디처럼 사용, 중복 불가
    hashed_password = Column(String) # 해싱된 비밀번호를 저장
