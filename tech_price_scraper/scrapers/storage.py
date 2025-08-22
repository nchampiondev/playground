from typing import Dict, Optional
import logging

from models import Product, Price
from database.operations import DatabaseOperations

logger = logging.getLogger(__name__)


class DataStorage:
    """Handles storage of scraped data"""
    
    def __init__(self, db_operations: DatabaseOperations):
        self.db_ops = db_operations
    
    def store_product_data(self, product_data: Dict, website_id, parser) -> Optional[Dict]:
        """Process and store product data"""
        try:
            if not product_data.get('price'):
                logger.warning(f"Skipping product {product_data['name']} - no price found")
                return None
            
            # Parse brand and model from name
            brand, model = parser.parse_brand_model(product_data['name'])
            
            # Create product
            product = Product(
                name=product_data['name'],
                category="gpu",
                brand=brand,
                model=model,
                specifications={}
            )
            
            # Check if product exists
            existing_product = self.db_ops.get_product_by_slug(product.slug)
            is_new_product = existing_product is None
            
            # Insert or update product
            product_id = self.db_ops.insert_or_update_product(product)
            
            # Create price record
            price = Price(
                product_id=product_id,
                website_id=website_id,
                price=product_data['price'],
                currency="EUR",
                product_url=product_data.get('url', ''),
                availability=product_data.get('availability', 'unknown'),
                raw_data=product_data
            )
            
            # Insert price
            self.db_ops.insert_price(price)
            
            # Update best price for product
            self.db_ops.update_product_best_price(product_id)
            
            return {
                'product_id': product_id,
                'is_new': is_new_product,
                'price_id': price.id
            }
            
        except Exception as e:
            logger.error(f"Error storing product {product_data['name']}: {e}")
            raise

