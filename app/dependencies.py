from fastapi import Depends, HTTPException, Cookie
from sqlmodel import Session, select
from .database import get_session
from .models.user import User
from .security import decode_token

def get_current_user(
    token: str = Cookie(None),
    session: Session = Depends(get_session)
) -> User:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def require_role(role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return role_checker