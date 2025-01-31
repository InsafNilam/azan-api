from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ....database import get_session
from ....models.user import User
from ....models.location import Location
from ....schemas.location import LocationResponse, LocationCreate, LocationUpdate
from ....dependencies import require_role

router = APIRouter()

# ✅ GET all locations
@router.get("/", response_model=List[LocationResponse])
def get_locations(session: Session = Depends(get_session)):
    return session.exec(select(Location)).all()

# ✅ GET a single location
@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, session: Session = Depends(get_session)):
    location = session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

# ✅ CREATE a location (Admin only)
@router.post("/", response_model=LocationResponse)
def create_location(location_create: LocationCreate, admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)):
    if session.get(Location, location_create.city):
        raise HTTPException(status_code=400, detail="Location already exists")
    
    new_location = Location(
        city=location_create.city,
        country=location_create.country,
        latitude=location_create.latitude,
        longitude=location_create.longitude,
        timezone=location_create.timezone
    )

    session.add(new_location)
    session.commit()
    session.refresh(new_location)
    return new_location

# ✅ UPDATE a location (Admin only)
@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    location_update: LocationUpdate,
    admin: User = Depends(require_role("admin")),
    session: Session = Depends(get_session)
):
    location = session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    if location_update.city:
        location.city = location_update.city
    if location_update.country:
        location.country = location_update.country
    if location_update.latitude:
        location.latitude = location_update.latitude
    if location_update.longitude:
        location.longitude = location_update.longitude
    if location_update.timezone:
        location.timezone = location_update.timezone

    session.add(location)
    session.commit()
    session.refresh(location)
    return location

# ✅ DELETE a location (Admin only)
@router.delete("/{location_id}")
def delete_location(location_id: int, admin: User = Depends(require_role("admin")), session: Session = Depends(get_session)):
    location = session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    session.delete(location)
    session.commit()
    return {"message": "Location deleted successfully"}