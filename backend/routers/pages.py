from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import crud, models, schemas, security
from ..database import get_db

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="backend/templates")

# --- 페이지 렌더링 엔드포인트 ---


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user_from_cookie),
):
    accommodations = crud.get_accommodations(db=db)
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "accommodations": accommodations,
            "current_user": current_user,
        },
    )


# --- ✨ 숙소 등록 페이지 기능을 다른 accommodation 관련 API보다 위로 이동 ---
@router.get("/accommodations/create", response_class=HTMLResponse)
def create_accommodation_page(
    request: Request,
    current_user: models.User = Depends(security.get_current_user_from_cookie),
):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(
        "create_accommodation.html", {"request": request, "current_user": current_user}
    )


@router.post("/accommodations/create")
def handle_create_accommodation(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user_from_cookie),
    name: str = Form(),
    location: str = Form(),
    price: int = Form(),
    description: str = Form(None),
):
    if not current_user:
        return RedirectResponse(url="/login")

    accommodation_data = schemas.AccommodationCreate(
        name=name, location=location, price=price, description=description
    )
    crud.create_accommodation(
        db=db, accommodation=accommodation_data, user_id=current_user.id
    )
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


# --- 회원가입 ---
@router.get("/register", response_class=HTMLResponse)
def register_page(
    request: Request,
    current_user: models.User = Depends(security.get_current_user_from_cookie),
):
    return templates.TemplateResponse(
        "register.html", {"request": request, "current_user": current_user}
    )


@router.post("/register", response_class=HTMLResponse)
def handle_registration(
    request: Request,
    email: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, email=email)
    if user:
        return templates.TemplateResponse(
            "register.html", {"request": request, "error": "이미 등록된 이메일입니다."}
        )
    crud.create_user(db, user=schemas.UserCreate(email=email, password=password))
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


# --- 로그인 ---
@router.get("/login", response_class=HTMLResponse)
def login_page(
    request: Request,
    current_user: models.User = Depends(security.get_current_user_from_cookie),
):
    return templates.TemplateResponse(
        "login.html", {"request": request, "current_user": current_user}
    )


# --- 로그인 처리 ---
@router.post("/login", response_class=HTMLResponse)
async def handle_login(
    request: Request,
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, email=username)
    if not user or not security.verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "이메일 또는 비밀번호가 잘못되었습니다."},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return response


# --- 로그아웃 ---
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="access_token")
    return response
