import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, Integer, String, Enum, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


from app.database import Base
from app.utils import generate_tracking_number


class PackageType(str, enum.Enum):
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
    
    
class Package(Base):
    __tablename__ = 'packages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False, index=True)
    package_type = Column(Enum(PackageType), nullable=False, index=True)
    origin_state = Column(String, nullable=False)
    origin_city = Column(String, nullable=False)
    destination_state = Column(String, nullable=False)
    destination_city = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    meta_data = Column(JSON, nullable=True)
    tracking_number = Column(String, nullable=True, unique=True)
    
    courier_id = Column(UUID(as_uuid=True), ForeignKey('couriers.uuid'), nullable=False)
    
    courier = relationship('Courier', back_populates='packages')
    

    @declared_attr
    def __mapper_args__(cls):
        def before_insert(mapper, connection, target):
            if not target.tracking_number:
                target.tracking_number = generate_tracking_number()
                
        from sqlalchemy import event
        event.listen(cls, 'before_insert', before_insert)
        return {}