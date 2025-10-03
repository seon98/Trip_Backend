# manage.py (전체 수정 코드)

from typing_extensions import Annotated

import typer
from sqlalchemy.orm import Session

import crud
import models
import schemas
import security
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# app = typer.Typer() 와 @app.command()를 제거하고,
# 함수 이름을 main으로 변경하거나 원하는 이름으로 둡니다.
def main(
    email: Annotated[str, typer.Option(help="관리자 계정으로 사용할 이메일 주소")],
    password: Annotated[str, typer.Option(help="새 관리자 계정의 비밀번호")]
):
    """
    새로운 관리자(admin) 계정을 생성합니다.
    """
    db: Session = SessionLocal()

    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        print(f"오류: 이메일 '{email}'은(는) 이미 존재합니다.")
        db.close()
        return

    user_in = schemas.UserCreate(email=email, password=password)

    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
        role="admin"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    print(f"🎉 성공: 관리자 계정 '{email}'이(가) 성공적으로 생성되었습니다!")

    db.close()

# 마지막 실행 부분을 typer.run(main)으로 변경합니다.
if __name__ == "__main__":
    typer.run(main)
