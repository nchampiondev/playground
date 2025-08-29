from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from pymongo import ReturnDocument
from typing import List, Dict, Optional
from datetime import datetime, timedelta, UTC
import logging

from models import Website, Product, Price

logger = logging.getLogger(__name__)


class DatabaseOperations:
    """Database operations for CRUD and data management"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.products = db_manager.products
        self.prices = db_manager.prices
        self.websites = db_manager.websites

    # --- Website operations ---
    def insert_website(self, website: Website) -> str:
        try:
            website_dict = website.dict(by_alias=True, exclude_unset=True)
            result = self.websites.insert_one(website_dict)
            return str(result.inserted_id)
        except DuplicateKeyError:
            existing = self.websites.find_one({"name": website.name})
            if existing:
                self.websites.update_one(
                    {"name": website.name},
                    {"$set": website.dict(exclude={"_id", "created_at"}, exclude_unset=True)}
                )
                return str(existing["_id"])
            raise

    def get_website_by_name(self, name: str) -> Optional[Website]:
        doc = self.websites.find_one({"name": name})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Website(**doc)
        return None

    # --- Product operations ---
    def insert_or_update_product(self, product: Product) -> str:
        try:
            now = datetime.now(UTC)

            product_dict = product.dict(by_alias=True, exclude_unset=True)
            product_dict.pop("created_at", None)
            product_dict.pop("updated_at", None)

            doc = self.products.find_one_and_update(
                {"slug": product.slug},
                {
                    "$setOnInsert": {"created_at": now},
                    "$set": {**product_dict, "updated_at": now},
                },
                upsert=True,
                return_document=ReturnDocument.AFTER,
                projection={"_id": 1}
            )

            return str(doc["_id"])

        except Exception as e:
            logger.exception(f"Error inserting/updating product {product.name}: {e}")
            raise

    def get_product_by_slug(self, slug: str) -> Optional[Product]:
        doc = self.products.find_one({"slug": slug})
        if doc:
            doc["_id"] = str(doc["_id"])
            return Product(**doc)
        return None

    # --- Price operations ---
    def insert_price(self, price: Price) -> str:
        try:
            price_dict = price.dict(by_alias=True, exclude_unset=True)
            # Convert str IDs -> ObjectId for storage
            price_dict["product_id"] = ObjectId(price.product_id)
            price_dict["website_id"] = ObjectId(price.website_id)

            result = self.prices.insert_one(price_dict)
            return str(result.inserted_id)
        except Exception as e:
            logger.exception(f"Error inserting price: {e}")
            raise

    def get_recent_prices(self, product_id: str, days: int = 30) -> List[Dict]:
        cutoff_date = datetime.now(UTC) - timedelta(days=days)
        prices = list(self.prices.find(
            {
                "product_id": ObjectId(product_id),
                "scraped_at": {"$gte": cutoff_date}
            }
        ).sort("scraped_at", -1))

        for p in prices:
            p["_id"] = str(p["_id"])
            p["product_id"] = str(p["product_id"])
            p["website_id"] = str(p["website_id"])
        return prices

    # --- Cache operations ---
    def update_product_best_price(self, product_id: str):
        try:
            pipeline = [
                {"$match": {"product_id": ObjectId(product_id)}},
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
                    "website_id": str(best_price["website_id"]),
                    "website_name": website["name"] if website else "unknown",
                    "last_updated": best_price["scraped_at"]
                }

                self.products.update_one(
                    {"_id": ObjectId(product_id)},
                    {"$set": {"current_best_price": current_best, "updated_at": datetime.now(UTC)}}
                )
        except Exception as e:
            logger.exception(f"Error updating best price for product {product_id}: {e}")

    # --- Cleanup operations ---
    def cleanup_old_prices(self, days_to_keep: int = 90):
        cutoff_date = datetime.now(UTC) - timedelta(days=days_to_keep)
        result = self.prices.delete_many({"scraped_at": {"$lt": cutoff_date}})
        return result.deleted_count
