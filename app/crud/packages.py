from typing import List, Optional, Tuple
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.packages import Package
from app.models.couriers import Courier
from app.schemas.packages import PackageCreate



def create_package(db: Session, package: PackageCreate, courier: Courier):
    package_data = package.dict()
    package_data.pop('courier_id', None)
    
    db_package = Package(**package_data, courier_id=courier.uuid)
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    
    return db_package


def get_packages(
    db: Session,
    origin_state: Optional[str] = None,
    destination_state: Optional[str] = None,
    package_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
) -> Tuple[List[Package], int]:
    
    query = db.query(Package).order_by(desc(Package.created_at))
        
    if origin_state:
        query = query.filter(Package.origin_state == origin_state)
        
    if destination_state:
        query = query.filter(Package.destination_state == destination_state)
        
    if package_type:
        query = query.filter(Package.package_type == package_type)
        
    if start_date:
        query = query.filter(Package.created_at >= start_date)
            
    if end_date:
        query = query.filter(Package.created_at <= end_date)  
        
    total = query.count()
    packages = query.offset((page - 1) * page_size).limit(page_size).all()
        
    return packages, total
        
    
def get_package(db: Session, package_id: UUID):
    package = db.query(Package).filter(Package.uuid == package_id).first()
    if package is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    return package
