# models.py (전체 수정 코드)

from sqlalchemy import Column, Integer, String, ForeignKey, Date
# 👇 sqlalchemy.orm에서 필요한 것들을 명확히 지정해줍니다.
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")

    accommodations = relationship("Accommodation", back_populates="owner")
    accommodation_bookings = relationship("AccommodationBooking", back_populates="user")
    flight_bookings = relationship("FlightBooking", back_populates="user")


class Accommodation(Base):
    __tablename__ = "accommodations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    price = Column(Integer)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="accommodations")
    bookings = relationship("AccommodationBooking", back_populates="accommodation")


class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, index=True)
    departure_airport = Column(String, index=True)
    arrival_airport = Column(String, index=True)
    departure_time = Column(String)
    arrival_time = Column(String)
    price = Column(Integer)

    bookings = relationship("FlightBooking", back_populates="flight")


class AccommodationBooking(Base):
    __tablename__ = "accommodation_bookings"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, default="pending")

    user_id = Column(Integer, ForeignKey("users.id"))
    accommodation_id = Column(Integer, ForeignKey("accommodations.id"))

    user = relationship("User", back_populates="accommodation_bookings")
    accommodation = relationship("Accommodation", back_populates="bookings")


class FlightBooking(Base):
    __tablename__ = "flight_bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_date = Column(Date, nullable=False)
    status = Column(String, default="pending")

    user_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))

    user = relationship("User", back_populates="flight_bookings")
    flight = relationship("Flight", back_populates="bookings")