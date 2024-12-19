from sqlalchemy.orm import Session

from app.models.couriers import Courier
from app.schemas import couriers as schemas
from app.auth import hash_password


def create_courier(db: Session, courier:schemas.CourierCreate):
    hashed_password = hash_password(courier.password)
    
    db_courier = Courier(
        first_name=courier.first_name,
        last_name=courier.last_name,
        email=courier.email,
        phone_number=courier.phone_number,
        password=hashed_password
    )
    
    db.add(db_courier)
    db.commit()
    db.refresh(db_courier)
    
    return db_courier


def get_courier_by_email(db: Session, email: str):
    return db.query(Courier).filter(Courier.email == email).first()


def get_courier_by_phone_number(db: Session, phone_number: str):
    return db.query(Courier).filter(Courier.phone_number == phone_number).first()