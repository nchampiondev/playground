from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class ScrapingResult(BaseModel):
    """Model for scraping operation results"""
    website: str
    success: bool
    products_found: int
    products_processed: int
    products_updated: int
    products_created: int
    errors: List[str] = Field(default_factory=list)
    duration_seconds: float = 0.0
