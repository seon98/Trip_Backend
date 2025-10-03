# backend/routers/admin_pages.py (새 파일)

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
import security
from database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["admin-pages"],
    # 이 라우터의 모든 페이지에 쿠키 기반 관리자 인증을 요구합니다.
    dependencies=[
        Depends(security.get_current_admin_user_from_cookie)
    ],  # 👈 쿠키용 인증 함수 사용
)

templates = Jinja2Templates(directory="templates")


# --- 관리자 대시보드 메인 ---
@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_base.html", {"request": request})


# --- 사용자 관리 페이지 ---
@router.get("/users", response_class=HTMLResponse)
def admin_users_page(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse(
        "admin_users.html", {"request": request, "users": users}
    )
