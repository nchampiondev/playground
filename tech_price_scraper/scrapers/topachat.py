import time
import logging
from datetime import datetime

from models import Website
from database.operations import DatabaseOperations
from scrapers.base_scraper import BaseScraper, ScrapingResult
from scrapers.web_client import WebClient
from scrapers.parser import ProductParser
from scrapers.storage import DataStorage

logger = logging.getLogger(__name__)


class TopAchatScraper(BaseScraper):
    """Scraper for TopAchat GPU prices"""
    
    def __init__(self, db_operations: DatabaseOperations):
        super().__init__()
        self.website_name = "topachat"
        self.db_ops = db_operations
        
        # Initialize components
        self.web_client = WebClient(rate_limit_ms=1000, max_retries=3)
        self.parser = ProductParser()
        self.storage = DataStorage(db_operations)
        
        # Setup website configuration
        self.website = self.setup_website_config()
    
    def setup_website_config(self) -> Website:
        """Setup website configuration in database"""
        website_config = Website(
            name="topachat",
            display_name="TopAchat",
            base_url="https://www.topachat.com",
            country="FR",
            currency="EUR",
            scraping_config={
                "base_gpu_url": "https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wgfx_pcie.html",
                "rate_limit_ms": 1000,
                "max_retries": 3,
                "selectors": {
                    "product_container": ".product-item, .article",
                    "name": ".product-title, .art-name, h3",
                    "price": ".price, .art-price",
                    "availability": ".stock, .dispo",
                    "link": "a"
                }
            }
        )
        
        website_id = self.db_ops.insert_website(website_config)
        website_config.id = website_id
        return website_config
    
    def scrape_listings(self, max_pages: int = 5) -> ScrapingResult:
        """Scrape GPU listings from TopAchat"""
        start_time = time.time()
        result = ScrapingResult(
            website="topachat",
            success=False,
            products_found=0,
            products_processed=0,
            products_updated=0,
            products_created=0
        )
        
        try:
            base_url = self.website.scraping_config["base_gpu_url"]
            
            for page in range(1, max_pages + 1):
                logger.info(f"Scraping TopAchat GPU page {page}")
                
                # Build page URL
                if page == 1:
                    page_url = base_url
                else:
                    page_url = f"{base_url}?page={page}"
                
                # Fetch page
                response = self.web_client.get(page_url)
                if not response:
                    error_msg = f"Failed to fetch page {page}"
                    logger.error(error_msg)
                    result.errors.append(error_msg)
                    continue
                
                # Parse products
                products = self.parser.parse_topachat_listings(response.text, page_url)
                
                if not products:
                    logger.info(f"No products found on page {page}, stopping")
                    break
                
                result.products_found += len(products)
                
                # Process each product
                for product_data in products:
                    try:
                        stored_result = self.storage.store_product_data(
                            product_data, 
                            self.website.id, 
                            self.parser
                        )
                        
                        if stored_result:
                            result.products_processed += 1
                            if stored_result['is_new']:
                                result.products_created += 1
                            else:
                                result.products_updated += 1
                    
                    except Exception as e:
                        error_msg = f"Error processing product {product_data.get('name', 'unknown')}: {e}"
                        logger.error(error_msg)
                        result.errors.append(error_msg)
            
            result.success = True
            
        except Exception as e:
            error_msg = f"Scraping failed: {e}"
            logger.error(error_msg)
            result.errors.append(error_msg)
        
        finally:
            result.duration_seconds = time.time() - start_time
            
            # Update website last_scraped
            self.db_ops.websites.update_one(
                {"_id": self.website.id},
                {"$set": {"last_scraped": datetime.utcnow()}}
            )
            
            # Close web client
            self.web_client.close()
        
        return result

