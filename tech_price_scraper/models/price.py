from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from bson import ObjectId

from models.base import PyObjectId


class Price(BaseModel):
    """Price model for storing price history"""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    product_id: PyObjectId
    website_id: PyObjectId
    
    price: float
    currency: str = "EUR"
    product_url: str
    availability: str  # in_stock, out_of_stock, limited, pre_order, unknown
    condition: str = "new"  # new, used, refurbished, open_box
    shipping_cost: Optional[float] = None
    seller: Optional[str] = None
    
    # Metadata
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    scraper_version: str = "1.0.0"
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @validator('availability')
    def validate_availability(cls, v):
        valid_statuses = ['in_stock', 'out_of_stock', 'limited', 'pre_order', 'unknown']
        if v not in valid_statuses:
            raise ValueError(f'Availability must be one of: {valid_statuses}')
        return v
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

