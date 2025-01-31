from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LocationBase(BaseModel):
    city: str
    country: str
    latitude: float
    longitude: float
    timezone: str

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None

class LocationResponse(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True