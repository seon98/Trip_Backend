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
