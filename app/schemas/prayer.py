from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrayerTimeBase(BaseModel):
    location_id: int
    date: datetime
    fajr: datetime
    dhuhr: datetime
    asr: datetime
    maghrib: datetime
    isha: datetime
    calculation_method: str

class PrayerTimeCreate(PrayerTimeBase):
    pass

class BulkPrayerTimeCreate(BaseModel):
    city: str
    month: int
    date_range: str  # Example: "1-10"
    fajr: str
    dhuhr: str
    asr: str
    maghrib: str
    isha: str
    calculation_method: str

class PrayerTimeUpdate(BaseModel):
    id: int
    location_id: Optional[int] = None
    date: Optional[datetime] = None
    fajr: Optional[datetime] = None
    dhuhr: Optional[datetime] = None
    asr: Optional[datetime] = None
    maghrib: Optional[datetime] = None
    isha: Optional[datetime] = None
    calculation_method: Optional[str] = None

class BulkPrayerTimeUpdate(BaseModel):
    city: str
    month: int
    date_range: str  # Example: "1-10"
    fajr: Optional[str] = None
    dhuhr: Optional[str] = None
    asr: Optional[str] = None
    maghrib: Optional[str] = None
    isha: Optional[str] = None

class PrayerTimeResponse(PrayerTimeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
