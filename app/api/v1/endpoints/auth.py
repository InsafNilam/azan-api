from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ....database import get_session
from ....models.user import User
from ....schemas.user import UserCreate
from ....schemas.token import Token
from ....security import create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
def register(
    user: UserCreate,
    session: Session = Depends(get_session),
    response: Response = None
):
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=User.hash_password(user.password),
        role="panel"
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    token = create_access_token(data={"sub": new_user.username, "role": new_user.role})
    response.set_cookie(key="token", value=token, httponly=True)
    return Token(access_token=token, token_type="bearer")

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
    response: Response = None
):
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()
    
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username, "role": user.role})
    response.set_cookie(key="token", value=token, httponly=True)
    return Token(access_token=token, token_type="bearer")

@router.post("/logout")
def logout(response: Response = None):
    response.delete_cookie(key="token")
    return {"message": "Logged out"}