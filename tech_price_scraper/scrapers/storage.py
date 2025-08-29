from typing import Dict, Optional
import logging
import re
from datetime import datetime, UTC
from models import Product, Price
from database.operations import DatabaseOperations

logger = logging.getLogger(__name__)


class DataStorage:
    """Handles storage of scraped data"""

    def __init__(self, db_operations: DatabaseOperations):
        self.db_ops = db_operations

    def store_product_data(self, product_data: Dict, website_id: str, parser) -> Optional[Dict]:
        try:
            # Skip if no price
            if not product_data.get("price"):
                logger.warning(f"Skipping product {product_data.get('name', 'UNKNOWN')} - no price found")
                return None

            # Parse brand and model
            brand, model = parser.parse_brand_model(product_data["name"])

            # Generate slug
            slug = re.sub(r"[^\w\s-]", "", product_data["name"].lower())
            slug = f"{slug}-{product_data["gpu_ram"].lower()}"
            slug = re.sub(r"[\s_-]+", "-", slug).strip("-")

            # Build product model
            product = Product(
                name=product_data["name"],
                slug=slug,
                category="gpu",
                brand=brand,
                model=model,
                specifications={
                    'gpu_ram': product_data["gpu_ram"]
                }
            )

            # Insert or update product
            existing_product = self.db_ops.get_product_by_slug(product.slug)
            is_new_product = existing_product is None
            product_id: str = self.db_ops.insert_or_update_product(product)

            # Create price record
            price = Price(
                product_id=product_id,
                website_id=website_id,
                price=float(product_data["price"]),
                currency="EUR",
                product_url=product_data.get("url", ""),
                availability=product_data.get("availability", "unknown"),
                scraped_at=datetime.now(UTC)
            )

            price_id: str = self.db_ops.insert_price(price)

            # Update best price cache
            #self.db_ops.update_product_best_price(product_id)

            return {
                "product_id": product_id,
                "is_new": is_new_product,
                "price_id": price_id
            }

        except Exception as e:
            logger.exception(f"Error storing product {product_data.get('name', 'UNKNOWN')}: {e}")
            raise
