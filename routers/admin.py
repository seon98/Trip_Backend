# backend/routers/admin.py (전체 수정 코드)

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import schemas
import security
from database import get_db

router = APIRouter(
    prefix="/api/admin",  # 👈 /admin -> /api/admin 으로 변경
    tags=["admin"],
    dependencies=[Depends(security.get_current_admin_user)],
)


@router.get("/users", response_model=List[schemas.User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/bookings", response_model=List[schemas.AccommodationBooking])
def read_all_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bookings = crud.get_all_accommodation_bookings(db, skip=skip, limit=limit)
    return bookings
