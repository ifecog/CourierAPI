from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List
from uuid import UUID

from pydantic import BaseModel


class PackageType(str, Enum):
    electronics = 'electronics'
    clothing = 'clothing'
    food = 'food'
    books = 'books'
    furniture = 'furniture'
    cosmetics = 'cosmetics'
    documents = 'documents'
    jewelry = 'jewelry'
    tools = 'tools'
    toys = 'toys'
    pharmaceuticals = 'pharmaceuticals'
    household_items = 'household_items'
    sports_equipment = 'sports_equipment'
    artwork = 'artwork'
    musical_instruments = 'musical_instruments'
    automotive_parts = 'automotive_parts'
    perishables = 'perishables'
    beverages = 'beverages'
    industrial_supplies = 'industrial_supplies'
    pet_supplies = 'pet_supplies'
    gardening_supplies = 'gardening_supplies'
    others = 'others'
    

class PackageCreate(BaseModel):
    courier_id: Optional[UUID]
    package_type: PackageType
    origin_state: str
    origin_city: str
    destination_state: str
    destination_city: str
    meta_data: Optional[Dict] = None
    
    
class PackageOut(PackageCreate):
    id: int
    uuid: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
        
class ResponseModel(BaseModel):
    status: str
    message: str
    data: PackageOut


class PaginatedResponse(BaseModel):
    status: str
    message: str
    data: List[PackageOut]
    page: int
    page_size: int
    total: int
    total_pages: int
    
     
