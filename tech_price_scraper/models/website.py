from datetime import datetime, UTC
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Website(BaseModel):
    """Website model for storing scraper configuration"""

    id: Optional[str] = Field(default=None, alias="_id")  # string for JSON
    name: str
    display_name: str
    base_url: str
    country: str = "FR"
    currency: str = "EUR"

    scraping_config: Dict[str, Any] = Field(default_factory=dict)

    active: bool = True
    last_scraped: Optional[datetime] = None
    error_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Config:
        populate_by_name = True
