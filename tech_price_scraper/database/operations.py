from pymongo.errors import DuplicateKeyError
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

from models import Website, Product, Price, PyObjectId

logger = logging.getLogger(__name__)


class DatabaseOperations:
    """Database operations for CRUD and data management"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.products = db_manager.products
        self.prices = db_manager.prices
        self.websites = db_manager.websites
    
    # Website operations
    def insert_website(self, website: Website) -> PyObjectId:
        """Insert or update a website configuration"""
        try:
            website_dict = website.dict(by_alias=True, exclude_unset=True)
            result = self.websites.insert_one(website_dict)
            logger.info(f"Website {website.name} inserted with ID: {result.inserted_id}")
            return result.inserted_id
        except DuplicateKeyError:
            # Update existing website
            existing = self.websites.find_one({"name": website.name})
            if existing:
                self.websites.update_one(
                    {"name": website.name},
                    {"$set": website.dict(exclude={"_id", "created_at"}, exclude_unset=True)}
                )
                logger.info(f"Website {website.name} updated")
                return existing["_id"]
            raise
    
    def get_website_by_name(self, name: str) -> Optional[Website]:
        """Get website by name"""
        doc = self.websites.find_one({"name": name})
        if doc:
            return Website(**doc)
        return None
    
    # Product operations
    def insert_or_update_product(self, product: Product) -> PyObjectId:
        """Insert new product or update existing one"""
        try:
            product.updated_at = datetime.utcnow()
            product_dict = product.dict(by_alias=True, exclude_unset=True)
            
            # Try to find existing product by slug
            existing = self.products.find_one({"slug": product.slug})
            
            if existing:
                # Update existing product
                self.products.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {k: v for k, v in product_dict.items() if k != "_id"}}
                )
                logger.debug(f"Product {product.name} updated")
                return existing["_id"]
            else:
                # Insert new product
                result = self.products.insert_one(product_dict)
                logger.info(f"New product {product.name} inserted with ID: {result.inserted_id}")
                return result.inserted_id
                
        except Exception as e:
            logger.error(f"Error inserting/updating product {product.name}: {e}")
            raise
    
    def get_product_by_slug(self, slug: str) -> Optional[Product]:
        """Get product by slug"""
        doc = self.products.find_one({"slug": slug})
        if doc:
            return Product(**doc)
        return None
    
    # Price operations
    def insert_price(self, price: Price) -> PyObjectId:
        """Insert a new price record"""
        try:
            price_dict = price.dict(by_alias=True, exclude_unset=True)
            result = self.prices.insert_one(price_dict)
            logger.debug(f"Price record inserted with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error inserting price: {e}")
            raise
    
    def get_recent_prices(self, product_id: PyObjectId, days: int = 30) -> List[Dict]:
        """Get recent prices for a product"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        prices = list(self.prices.find(
            {
                "product_id": product_id,
                "scraped_at": {"$gte": cutoff_date}
            }
        ).sort("scraped_at", -1))
        
        return prices
    
    # Cache operations
    def update_product_best_price(self, product_id: PyObjectId):
        """Update the current best price for a product"""
        try:
            # Find the lowest current price for this product
            pipeline = [
                {"$match": {"product_id": product_id}},
                {"$sort": {"scraped_at": -1}},
                {"$group": {
                    "_id": "$website_id",
                    "latest_price": {"$first": "$$ROOT"}
                }},
                {"$replaceRoot": {"newRoot": "$latest_price"}},
                {"$sort": {"price": 1}},
                {"$limit": 1}
            ]
            
            result = list(self.prices.aggregate(pipeline))
            
            if result:
                best_price = result[0]
                website = self.websites.find_one({"_id": best_price["website_id"]})
                
                current_best = {
                    "price": best_price["price"],
                    "currency": best_price["currency"],
                    "website_id": best_price["website_id"],
                    "website_name": website["name"] if website else "unknown",
                    "last_updated": best_price["scraped_at"]
                }
                
                self.products.update_one(
                    {"_id": product_id},
                    {"$set": {"current_best_price": current_best, "updated_at": datetime.utcnow()}}
                )
                
                logger.debug(f"Updated best price for product {product_id}")
            
        except Exception as e:
            logger.error(f"Error updating best price for product {product_id}: {e}")
    
    # Cleanup operations
    def cleanup_old_prices(self, days_to_keep: int = 90):
        """Clean up old price records to manage storage"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        result = self.prices.delete_many({"scraped_at": {"$lt": cutoff_date}})
        logger.info(f"Cleaned up {result.deleted_count} old price records")
        return result.deleted_count

