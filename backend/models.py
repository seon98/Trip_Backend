# backend/models.py

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # User 모델에서 자신이 소유한 Accommodation 목록을 참조합니다.
    accommodations = relationship("Accommodation", back_populates="owner")


class Accommodation(Base):
    __tablename__ = "accommodations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    price = Column(Integer)
    description = Column(String, nullable=True)

    # users 테이블의 id 컬럼을 참조하는 외래 키를 추가합니다.
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Accommodation 모델에서 소유자인 User 정보를 참조합니다.
    owner = relationship("User", back_populates="accommodations")


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    departure_airport = Column(String, index=True)
    arrival_airport = Column(String, index=True)
    departure_time = Column(String)
    arrival_time = Column(String)
    price = Column(Integer)
