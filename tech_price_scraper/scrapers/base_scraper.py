from abc import ABC, abstractmethod
from models import ScrapingResult

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
