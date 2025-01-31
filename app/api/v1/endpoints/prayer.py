from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, delete
from typing import List
from ....database import get_session
from ....models.user import User
from ....models.location import Location
from ....models.prayer import PrayerTime
from ....schemas.prayer import PrayerTimeResponse, PrayerTimeCreate, BulkPrayerTimeCreate, PrayerTimeUpdate, BulkPrayerTimeUpdate
from ....dependencies import require_role

router = APIRouter()

# ✅ GET all prayer times
@router.get("/", response_model=List[PrayerTimeResponse])
def get_prayer_times(session: Session = Depends(get_session)):
    return session.exec(select(PrayerTime)).all()

# ✅ GET a single prayer time
@router.get("/{prayer_time_id}", response_model=PrayerTimeResponse)
def get_prayer_time(prayer_time_id: int, session: Session = Depends(get_session)):
    prayer_time = session.get(PrayerTime, prayer_time_id)
    if not prayer_time:
        raise HTTPException(status_code=404, detail="Prayer time not found")
    return prayer_time

# ✅ CREATE a prayer time (Admin only)
@router.post("/", response_model=PrayerTimeResponse)
def create_prayer_time(prayer_time_create: PrayerTimeCreate, admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)):
    if session.get(PrayerTime, prayer_time_create.city):
        raise HTTPException(status_code=400, detail="Prayer time already exists")
    
    new_prayer_time = PrayerTime(
        city=prayer_time_create.city,
        country=prayer_time_create.country,
        fajr=prayer_time_create.fajr,
        dhuhr=prayer_time_create.dhuhr,
        asr=prayer_time_create.asr,
        maghrib=prayer_time_create.maghrib,
        isha=prayer_time_create.isha
    )

    session.add(new_prayer_time)
    session.commit()
    session.refresh(new_prayer_time)
    return new_prayer_time

# ✅ UPDATE a prayer time (Admin only)
@router.put("/{prayer_time_id}", response_model=PrayerTimeResponse)
def update_prayer_time(
    prayer_time_id: int,
    prayer_time_update: PrayerTimeUpdate,
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)
):
    prayer_time = session.get(PrayerTime, prayer_time_id)
    if not prayer_time:
        raise HTTPException(status_code=404, detail="Prayer time not found")
    
    if prayer_time_update.city:
        prayer_time.city = prayer_time_update.city
    if prayer_time_update.country:
        prayer_time.country = prayer_time_update.country
    if prayer_time_update.fajr:
        prayer_time.fajr = prayer_time_update.fajr
    if prayer_time_update.dhuhr:
        prayer_time.dhuhr = prayer_time_update.dhuhr
    if prayer_time_update.asr:
        prayer_time.asr = prayer_time_update.asr
    if prayer_time_update.maghrib:
        prayer_time.maghrib = prayer_time_update.maghrib
    if prayer_time_update.isha:
        prayer_time.isha = prayer_time_update.isha

    session.add(prayer_time)
    session.commit()
    session.refresh(prayer_time)
    return prayer_time

# ✅ DELETE a prayer time (Admin only)
@router.delete("/{prayer_time_id}")
def delete_prayer_time(prayer_time_id: int, admin: User = Depends(require_role("admin")), session: Session = Depends(get_session)):
    prayer_time = session.get(PrayerTime, prayer_time_id)
    if not prayer_time:
        raise HTTPException(status_code=404, detail="Prayer time not found")
    session.delete(prayer_time)
    session.commit()
    return {"message": "Prayer time deleted successfully"}

# ✅ DELETE all prayer times (Admin only)
@router.delete("/")
def delete_all_prayer_times(admin: User = Depends(require_role("admin")), session: Session = Depends(get_session)):
    session.exec(delete(PrayerTime))
    session.commit()
    return {"message": "All prayer times deleted successfully"}

# ✅ GET prayer times by city
@router.get("/city/{city}", response_model=List[PrayerTimeResponse])
def get_prayer_times_by_city(
    city: str, 
    session: Session = Depends(get_session)
):
    # Join PrayerTime with Location to filter by city
    prayer_times = session.exec(
        select(PrayerTime)
        .join(Location)
        .where(Location.city.lower() == city.lower())
    ).all()
    
    if not prayer_times:
        raise HTTPException(status_code=404, detail=f"No prayer times found for city: {city}")
    
    return prayer_times

# ✅ GET prayer times by country
@router.get("/country/{country}", response_model=List[PrayerTimeResponse])
def get_prayer_times_by_country(
    country: str, 
    session: Session = Depends(get_session)
):
    # Join PrayerTime with Location to filter by country
    prayer_times = session.exec(
        select(PrayerTime)
        .join(Location)
        .where(Location.country.lower() == country.lower())
    ).all()
    
    if not prayer_times:
        raise HTTPException(status_code=404, detail=f"No prayer times found for country: {country}")
    
    return prayer_times

# 🔐 CREATE Bulk Prayer Times (Admin Only)
@router.post("/bulk", response_model=List[PrayerTime])
def create_bulk_prayer_times(
    prayer_times: List[BulkPrayerTimeCreate],
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)
):
    try:
        created_times = []
        for prayer_time_data in prayer_times:
            # 🔍 Step 1: Find Location ID by City
            location = session.exec(select(Location).where(Location.city == prayer_time_data.city)).first()
            if not location:
                raise HTTPException(status_code=404, detail=f"City '{prayer_time_data.city}' not found")

            # 🗓 Step 2: Parse Date Range (e.g., "1-10" → [1,2,3...10])
            try:
                start_day, end_day = map(int, prayer_time_data.date_range.split('-'))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date_range format. Use 'start-end' (e.g., '1-10').")

            # Generate Dates for the Given Month
            bulk_dates = [date(2025, prayer_time_data.month, day) for day in range(start_day, end_day + 1)]

            # 🔍 Step 3: Check for Existing Records
            existing_records = session.exec(
                select(PrayerTime).where(
                    (PrayerTime.location_id == location.id) & 
                    (PrayerTime.date.in_(bulk_dates))
                )
            ).all()

            if existing_records:
                raise HTTPException(status_code=409, detail="Some prayer times already exist. Operation aborted.")

            # ✅ Step 4: Bulk Insert New Records
            for prayer_date in bulk_dates:
                new_prayer_time = PrayerTime(
                    location_id=location.id,
                    date=prayer_date,
                    fajr=prayer_time_data.fajr,
                    dhuhr=prayer_time_data.dhuhr,
                    asr=prayer_time_data.asr,
                    maghrib=prayer_time_data.maghrib,
                    isha=prayer_time_data.isha,
                    calculation_method=prayer_time_data.calculation_method
                )
                session.add(new_prayer_time)
                created_times.append(new_prayer_time)

        # 📝 Commit All Inserts
        session.commit()
        for prayer_time in created_times:
            session.refresh(prayer_time)

        return created_times

    except HTTPException as e:
        session.rollback()  # 🔄 Rollback Everything if Error Occurs
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# 🔐 EDIT Bulk Prayer Times (Admin Only)
@router.put("/bulk", response_model=List[PrayerTime])
def update_bulk_prayer_times(
    prayer_times: List[BulkPrayerTimeUpdate],
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)
):
    try:
        updated_times = []
        for prayer_time_update in prayer_times:
            # Find Location ID by City
            location = session.exec(select(Location).where(Location.city == prayer_time_update.city)).first()
            if not location:
                raise HTTPException(status_code=404, detail=f"City '{prayer_time_update.city}' not found")

            # Parse Date Range 
            try:
                start_day, end_day = map(int, prayer_time_update.date_range.split('-'))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date_range format. Use 'start-end' (e.g., '1-10').")

            # Generate Dates for the Given Month
            bulk_dates = [date(2025, prayer_time_update.month, day) for day in range(start_day, end_day + 1)]

            # Iterate Through Dates and Update or Create Records
            for single_date in bulk_dates:
                # Try to find existing record
                existing_prayer = session.exec(
                    select(PrayerTime).where(
                        (PrayerTime.location_id == location.id) & 
                        (PrayerTime.date == single_date)
                    )
                ).first()

                # If no existing record, create a new one
                if not existing_prayer:
                    existing_prayer = PrayerTime(
                        location_id=location.id,
                        date=single_date
                    )
                    session.add(existing_prayer)

                # Update prayer times
                if prayer_time_update.fajr:
                    existing_prayer.fajr = prayer_time_update.fajr
                if prayer_time_update.dhuhr:
                    existing_prayer.dhuhr = prayer_time_update.dhuhr
                if prayer_time_update.asr:
                    existing_prayer.asr = prayer_time_update.asr
                if prayer_time_update.maghrib:
                    existing_prayer.maghrib = prayer_time_update.maghrib
                if prayer_time_update.isha:
                    existing_prayer.isha = prayer_time_update.isha

                updated_times.append(existing_prayer)

        # Commit All Updates
        session.commit()
        for prayer_time in updated_times:
            session.refresh(prayer_time)
        return updated_times

    except HTTPException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# 🔐 DELETE Bulk Prayer Times (Admin Only)
@router.delete("/bulk") 
def delete_bulk_prayer_times(
    city: str,
    month: int,
    date_range: str,
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)
):
    try:
        # Find Location ID by City
        location = session.exec(select(Location).where(Location.city == city)).first()
        if not location:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found")

        # Parse Date Range 
        try:
            start_day, end_day = map(int, date_range.split('-'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_range format. Use 'start-end' (e.g., '1-10').")

        # Generate Dates for the Given Month
        bulk_dates = [date(2025, month, day) for day in range(start_day, end_day + 1)]

        # Find and Delete All Records
        existing_prayers = session.exec(
            select(PrayerTime).where(
                (PrayerTime.location_id == location.id) & 
                (PrayerTime.date.in_(bulk_dates))
            )
        ).all()

        if not existing_prayers:
            raise HTTPException(status_code=404, detail="No prayer times found for the specified date range")

        for prayer_time in existing_prayers:
            session.delete(prayer_time)
        session.commit()

        return {"message": f"Deleted {len(existing_prayers)} prayer times"}

    except HTTPException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# 🌐 View Single Prayer Time (Current Date/Specific Date)
@router.get("/single", response_model=PrayerTimeResponse)
def get_single_prayer_time(
    location_id: int,
    date: date = None,
    session: Session = Depends(get_session)
):
    # If no date provided, use current date
    if date is None:
        date = datetime.now().date()
    
    prayer_time = session.exec(
        select(PrayerTime)
        .where(
            PrayerTime.location_id == location_id,
            PrayerTime.date == date
        )
    ).first()
    
    if not prayer_time:
        raise HTTPException(status_code=404, detail="Prayer time not found")
    
    return prayer_time

# 🌐 View Multiple Prayer Times (Date Range)
@router.get("/multiple", response_model=List[PrayerTimeResponse])
def get_prayer_times_by_date_range(
    location_id: int,
    start_date: date,
    end_date: date,
    session: Session = Depends(get_session)
):
    prayer_times = session.exec(
        select(PrayerTime)
        .where(
            PrayerTime.location_id == location_id,
            PrayerTime.date >= start_date,
            PrayerTime.date <= end_date
        )
        .order_by(PrayerTime.date)
    ).all()
    
    if not prayer_times:
        raise HTTPException(status_code=404, detail="No prayer times found in the specified date range")
    
    return prayer_times

