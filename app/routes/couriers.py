from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from sqlalchemy.orm import Session

from app.crud import couriers as crud
from app.database import engine, Base
from app.dependencies import get_db
from app.schemas import couriers as schemas
from app.auth import verify_password, create_access_token
from app.models.couriers import Courier


Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/register", response_model=schemas.CourierOut)
def register_courier(courier: schemas.CourierCreate, db: Session = Depends(get_db)):
    return crud.create_courier(db, courier)

@router.post('/signin', response_model=schemas.Token)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.email == form_data.username).first()
    if not courier or not verify_password(form_data.password, courier.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(courier.email)})
    return {"access_token": access_token, "token_type": "bearer"}