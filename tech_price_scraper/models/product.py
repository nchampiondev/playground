from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from bson import ObjectId

from models.base import PyObjectId


class Product(BaseModel):
    """Product model for storing product information"""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    slug: str
    category: str
    brand: str
    model: str
    specifications: Dict[str, Any] = Field(default_factory=dict)
    
    # Cache for performance
    current_best_price: Optional[Dict[str, Any]] = None
    price_stats: Optional[Dict[str, Any]] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('slug', pre=True, always=True)
    def generate_slug(cls, v, values):
        if not v and 'name' in values:
            import re
            slug = re.sub(r'[^\w\s-]', '', values['name'].lower())
            slug = re.sub(r'[\s_-]+', '-', slug)
            return slug.strip('-')
        return v
    
    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

