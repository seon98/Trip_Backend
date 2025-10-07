from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, models, schemas, security
from database import get_db

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="backend/templates")


# ... (home, register, login, logout, create_accommodation 등 기존 코드는 그대로 둡니다) ...

# --- ✨ 여기에 새로운 '내 예약 목록' 페이지 엔드포인트를 추가합니다 ✨ ---
@router.get("/my-bookings", response_class=HTMLResponse)
def my_bookings_page(
        request: Request,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(security.get_current_user_from_cookie)
):
    if not current_user:
        return RedirectResponse(url="/login")

    # 현재 로그인한 유저의 숙소/항공권 예약 목록을 DB에서 가져옵니다.
    accommodation_bookings = crud.get_user_accommodation_bookings(db, user_id=current_user.id)
    flight_bookings = crud.get_user_flight_bookings(db, user_id=current_user.id)

    return templates.TemplateResponse("my_bookings.html", {
        "request": request,
        "current_user": current_user,
        "accommodation_bookings": accommodation_bookings,
        "flight_bookings": flight_bookings
    })