from sqlmodel import SQLModel, Session
from app.database import engine
from app.models.user import User
from app.models.location import Location

def reset_database():
    """Drop all tables and recreate them"""
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def seed_database(session:Session):
    """Seed initial data into the database"""
    # Example seed data
    users = [
        User(
            username="admin", 
            email="admin@azanlanka.lk", 
            hashed_password=User.hash_password("47@n2EEr"),
            role="admin"
        ),
    ]

    locations = [
        Location(
            city="Colombo", 
            country="Sri Lanka", 
            latitude=6.9271, 
            longitude=79.8612, 
            timezone="Asia/Colombo"
        ),
        Location(
            city="Batticaloa",
            country="Sri Lanka",
            latitude=7.7172,
            longitude=81.7006,
            timezone="Asia/Colombo"
        )
    ]

    session.add_all(users)
    session.add_all(locations)
    session.commit()
    session.close()

