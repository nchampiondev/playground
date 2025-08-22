from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId

from models.base import PyObjectId


class Website(BaseModel):
    """Website model for storing scraper configuration"""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    display_name: str
    base_url: str
    country: str = "FR"
    currency: str = "EUR"
    
    scraping_config: Dict[str, Any] = Field(default_factory=dict)
    
    active: bool = True
    last_scraped: Optional[datetime] = None
    error_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

