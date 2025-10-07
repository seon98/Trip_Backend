from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud, models, security
from database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["admin-pages"],
    dependencies=[Depends(security.get_current_admin_user_from_cookie)]
)

templates = Jinja2Templates(directory="backend/templates")

# --- 관리자 대시보드 메인 ---
@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_base.html", {"request": request})

# --- 사용자 관리 페이지 ---
@router.get("/users", response_class=HTMLResponse)
def admin_users_page(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": users})

# --- 예약 관리 페이지 ---
@router.get("/bookings", response_class=HTMLResponse)
def admin_bookings_page(request: Request, db: Session = Depends(get_db)):
    bookings = crud.get_all_accommodation_bookings(db)
    return templates.TemplateResponse("admin_bookings.html", {"request": request, "bookings": bookings})

# --- ✨ 여기에 새로운 예약 상태 변경 엔드포인트를 추가합니다 ✨ ---
@router.post("/bookings/{booking_id}/update-status")
def handle_update_booking_status(
    booking_id: int,
    status: str = Form(),
    db: Session = Depends(get_db)
):
    crud.update_accommodation_booking_status(db=db, booking_id=booking_id, status=status)
    # 상태 변경 후, 다시 예약 관리 페이지로 리다이렉트
    return RedirectResponse(url="/admin/bookings", status_code=status.HTTP_303_SEE_OTHER)