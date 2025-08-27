from datetime import datetime, UTC
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Product(BaseModel):
    """Product model for storing product information"""

    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    slug: str
    category: str
    brand: str
    model: str
    specifications: Dict[str, Any] = Field(default_factory=dict)

    # Cache for performance
    current_best_price: Optional[Dict[str, Any]] = None
    price_stats: Optional[Dict[str, Any]] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Config:
        populate_by_name = True
