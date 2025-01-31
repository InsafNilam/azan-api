from datetime import datetime, date, time, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class PrayerTime(SQLModel, table=True):
    __tablename__ = "prayer_times"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key="locations.id")
    date: date
    fajr: time
    dhuhr: time
    asr: time
    maghrib: time
    isha: time
    calculation_method: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))