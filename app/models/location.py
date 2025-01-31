from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class Location(SQLModel, table=True):
    __tablename__ = "locations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    city: str = Field(unique=True, index=True)
    country: str
    latitude: float
    longitude: float
    timezone: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))