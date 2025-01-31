from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field
from ..security import verify_password, get_password_hash

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return get_password_hash(password)