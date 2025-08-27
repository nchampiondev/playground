from datetime import datetime, UTC
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Price(BaseModel):
    """Price model for storing price history"""

    id: Optional[str] = Field(default=None, alias="_id")
    product_id: str   # store IDs as str
    website_id: str

    price: float
    currency: str = "EUR"
    product_url: str
    availability: str  # in_stock, out_of_stock, limited, pre_order, unknown
    condition: str = "new"  # new, used, refurbished, open_box
    shipping_cost: Optional[float] = None
    seller: Optional[str] = None

    # Metadata
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    scraper_version: str = "1.0.0"
    raw_data: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        populate_by_name = True
