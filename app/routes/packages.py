from datetime import datetime
from decouple import config
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.schemas.packages import PackageCreate, PackageOut, ResponseModel, PaginatedResponse
from app.database import engine, Base
from app.dependencies import get_db
from app.crud.packages import create_package, get_packages, get_package
from app.models.couriers import Courier
from app.auth import get_current_courier
from app.logging import logger
from app.services.rabbitmq_producer import publish_message


Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post('/create', response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
def create_new_package(package: PackageCreate, db: Session = Depends(get_db), current_courier: Courier = Depends(get_current_courier)):
    new_package = create_package(db, package, current_courier)
    
    message = {
        'event': 'package-registration',
        'data': {
            'courier_id': str(new_package.courier_id),                
            'class': new_package.package_type.value,
            'origin_state': new_package.origin_state,
            'origin_city': new_package.origin_city,
            'destination_state': new_package.destination_state,
            'destination_city': new_package.destination_city,
            'tracking_number': new_package.tracking_number,
            'meta_data': new_package.meta_data,
            'created_at': str(new_package.created_at),
        }
    }
    
    try:
        publish_message(config('RABBITMQ_QUEUE'), message)
    except Exception as e:
        logger.error(f"RabbitMQ publish failed for the package {new_package.uuid}: {e}")
        raise HTTPException(
            status_code=500,
            detail='Package created, but failed to queue for processing'
        )
        
    package_data = PackageOut.from_orm(new_package)
    
    return ResponseModel(
        status="success",
        message="Package created successfully",
        data=package_data
    )


@router.get('/', response_model=PaginatedResponse, status_code=status.HTTP_200_OK)
def read_packages(
    origin_state: Optional[str] = None,
    destination_state: Optional[str] = None,
    package_type: Optional[str] = None,
    start_date: Optional[datetime] = Query(None, description="Start date in ISO format (e.g., 2024-12-01T00:00:00)"),
    end_date: Optional[datetime] = Query(None, description="End date in ISO format (e.g., 2024-12-10T23:59:59)"),
    page: int = Query(1, ge=1, description="Page number (1-based index)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page (max 100)"),
    db: Session = Depends(get_db)
):
    packages, total = get_packages(
        db=db, 
        origin_state=origin_state, 
        destination_state=destination_state, 
        package_type=package_type, 
        start_date=start_date,
        end_date=end_date,
        page=page,
        page_size=page_size,
    )
    
    if not packages:
        raise HTTPException(status_code=404, detail="No packages found for the given criteria.")

    package_data = [PackageOut.from_orm(package) for package in packages]

    total_pages = (total + page_size - 1)
    
    return PaginatedResponse(
        status="success",
        message="Packages retrieved successfully",
        data=package_data,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )
    

@router.get('/{package_id}', response_model=ResponseModel, status_code=status.HTTP_200_OK)
def read_package(package_id: UUID, db: Session = Depends(get_db)):
    package = get_package(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    
    package_data = PackageOut.from_orm(package)
    
    return ResponseModel(
        status="success",
        message="Package retrieved successfully",
        data=package_data
    )


# @router.delete('/{package_id}/delete', response_model=dict, status_code=status.HTTP_200_OK)
# def delete_package(package_id: UUID, db: Session = Depends(get_db)):
#     package = get_package(db, package_id)
#     if not package:
#         raise HTTPException(status_code=404, detail='Package not found')
    
#     db.delete(package)
#     db.commit()
    
#     FastAPICache.clear(f'read_package:{package_id}')
    
#     return {
#         "status": "success",
#         "message": "Package deleted successfully",
#         "data": []
#     }

