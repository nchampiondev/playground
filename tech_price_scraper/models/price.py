from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Price(BaseModel):
    """Price model for storing price history"""

    id: Optional[str] = Field(default=None, alias="_id")
    product_id: str   # store IDs as str
    website_id: str
    price: float
    currency: str
    product_url: str
    availability: str  # in_stock, out_of_stock, limited, pre_order, unknown
    condition: str = "new"  # new, used, refurbished, open_box
    shipping_cost: Optional[float] = None
    seller: Optional[str] = None
    scraped_at: datetime

    class Config:
        populate_by_name = True
