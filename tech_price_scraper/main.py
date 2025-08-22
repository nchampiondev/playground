#!/usr/bin/env python3
"""
Tech Price Scraper - Main Application
Scrapes GPU prices from various websites and stores them in MongoDB
"""

import sys
from datetime import datetime

from utils.logging import setup_logging
from database import DatabaseManager, DatabaseOperations
from scrapers import TopAchatScraper


def main():
    """Main scraper function"""
    logger = setup_logging()
    logger.info("Starting tech price scraper")
    
    # Initialize database
    db_manager = None
    try:
        db_manager = DatabaseManager()
        db_ops = DatabaseOperations(db_manager)
        logger.info("Database connection established")
        
        # Initialize and run scraper
        scraper = TopAchatScraper(db_ops)
        
        logger.info("Starting TopAchat GPU scraping")
        result = scraper.scrape_listings(max_pages=3)
        
        # Display results
        display_results(result, db_manager)
        
    except Exception as e:
        logger.error(f"Main execution failed: {e}")
        sys.exit(1)
    
    finally:
        if db_manager:
            db_manager.close()
            logger.info("Database connection closed")


def display_results(result, db_manager):
    """Display scraping results"""
    logger = setup_logging()
    
    # Log results
    logger.info("Scraping completed")
    logger.info(f"Success: {result.success}")
    logger.info(f"Products found: {result.products_found}")
    logger.info(f"Products processed: {result.products_processed}")
    logger.info(f"Products created: {result.products_created}")
    logger.info(f"Products updated: {result.products_updated}")
    logger.info(f"Duration: {result.duration_seconds:.2f} seconds")
    
    if result.errors:
        logger.warning(f"Errors encountered: {len(result.errors)}")
        for error in result.errors[:5]:  # Show first 5 errors
            logger.warning(f"Error: {error}")
    
    # Console output
    print("\n" + "="*60)
    print("TECH PRICE SCRAPER RESULTS")
    print("="*60)
    print(f"Website: {result.website}")
    print(f"Success: {result.success}")
    print(f"Products found: {result.products_found}")
    print(f"Products processed: {result.products_processed}")
    print(f"Products created: {result.products_created}")
    print(f"Products updated: {result.products_updated}")
    print(f"Duration: {result.duration_seconds:.2f}s")
    print(f"Errors: {len(result.errors)}")
    
    # Show recent products
    recent_products = list(db_manager.products.find().sort("created_at", -1).limit(5))
    if recent_products:
        print("\nRecent Products:")
        print("-" * 40)
        for product in recent_products:
            best_price = product.get('current_best_price', {})
            price_info = f"{best_price.get('price', 'N/A')} {best_price.get('currency', '')}"
            print(f"• {product['name'][:50]}...")
            print(f"  Brand: {product['brand']} | Model: {product['model']} | Price: {price_info}")
            print()
    
    # Show database statistics
    total_prices = db_manager.prices.count_documents({})
    today_prices = db_manager.prices.count_documents({
        "scraped_at": {"$gte": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)}
    })
    
    print(f"Database Statistics:")
    print(f"Total products: {db_manager.products.count_documents({})}")
    print(f"Total prices: {total_prices}")
    print(f"Prices added today: {today_prices}")
    print("="*60)


def test_database():
    """Test database connection"""
    logger = setup_logging()
    logger.info("Testing database connection...")
    
    try:
        db_manager = DatabaseManager()
        
        # Test basic operations
        test_product = {
            "name": "Test GPU Connection",
            "category": "gpu",
            "brand": "test",
            "model": "test-model",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = db_manager.products.insert_one(test_product)
        logger.info(f"Test insert successful: {result.inserted_id}")
        
        # Clean up test data
        db_manager.products.delete_one({"_id": result.inserted_id})
        logger.info("Test cleanup successful")
        
        db_manager.close()
        print("✓ Database connection test passed!")
        return True
        
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        print(f"✗ Database connection test failed: {e}")
        return False


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test-db":
            success = test_database()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--help":
            print("Tech Price Scraper")
            print("Usage:")
            print("  python main.py           # Run the scraper")
            print("  python main.py --test-db # Test database connection")
            print("  python main.py --help    # Show this help")
            sys.exit(0)
    
    # Run main scraper
    main()

