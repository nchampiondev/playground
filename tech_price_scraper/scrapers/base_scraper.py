from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import List, Dict
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
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    duration_seconds: float = 0.0


class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    def __init__(self):
        self.website_name = ""
    
    @abstractmethod
    def scrape_listings(self, max_pages: int = 5) -> ScrapingResult:
        """Scrape product listings from the website"""
        pass
    
    @abstractmethod
    def setup_website_config(self):
        """Setup website configuration in database"""
        pass

