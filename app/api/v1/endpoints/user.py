from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ....database import get_session
from ....models.user import User
from ....schemas.user import UserResponse, UserUpdate, UpdatePassword, AdminUserCreate
from ....dependencies import get_current_user, require_role

router = APIRouter()

# ✅ GET current user info
@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# ✅ UPDATE current user
@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        current_user.email = user_update.email

    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return 

# ✅ UPDATE current user password
@router.put("/me/password", response_model=UserResponse)
def update_password(password_update: UpdatePassword, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    current_user.hashed_password = User.hash_password(password_update.password)
    session.add(current_user)
    session.commit()
    return {"message": "Password updated successfully"}

# ✅ DELETE current user
@router.delete("/me")
def delete_current_user(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    session.delete(current_user)
    session.commit()
    return {"message": "User deleted successfully"}

# ✅ GET all users (admin/panel) (Admin only)
@router.get("/", response_model=List[UserResponse])
def get_users(
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)
):
    return session.exec(select(User)).all()

# ✅ GET a single user (admin/panel) (Admin only)
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, admin: User = Depends(require_role("admin")), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ✅ CREATE a new user (admin/panel) (Admin only)
@router.post("/", response_model=UserResponse)
def create_user(
    user: AdminUserCreate,
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)
):
    if session.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=User.hash_password(user.password),
        role=user.role
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# ✅ UPDATE an existing user (admin/panel) (Admin only)
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.username:
        user.username = user_update.username
    if user_update.email:
        user.email = user_update.email
    if user_update.role:
        user.role = user_update.role

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# ✅ CREATE a new user (admin/panel) (Admin only)
@router.delete("/{user_id}")
def delete_user(user_id: int, admin: User = Depends(require_role("admin")), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}