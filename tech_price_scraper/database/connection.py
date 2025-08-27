from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages MongoDB connection and basic setup"""
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", database_name: str = "tech_prices"):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.products = self.db.products
        self.prices = self.db.prices
        self.websites = self.db.websites
        
        # Create indexes on initialization
        self._create_indexes()
    
    def _create_indexes(self):
        """Create necessary indexes for optimal performance"""
        try:
            # Products collection indexes
            self.products.create_index([("category", 1), ("brand", 1)])
            self.products.create_index([("slug", 1)], unique=True)
            self.products.create_index([("current_best_price.price", 1)])
            self.products.create_index([("name", "text"), ("brand", "text"), ("model", "text")])
            
            # Prices collection indexes
            self.prices.create_index([("product_id", 1), ("scraped_at", -1)])
            self.prices.create_index([("website_id", 1), ("scraped_at", -1)])
            self.prices.create_index([("scraped_at", -1)])
            self.prices.create_index([("product_id", 1), ("website_id", 1), ("scraped_at", -1)])
            self.prices.create_index([("price", 1), ("currency", 1), ("scraped_at", -1)])
            
            # Websites collection indexes
            self.websites.create_index([("name", 1)], unique=True)
            self.websites.create_index([("active", 1)])
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.exception(f"Error creating indexes: {e}")
    
    def close(self):
        """Close database connection"""
        self.client.close()

