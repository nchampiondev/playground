from pymongo import MongoClient
from datetime import datetime

try:
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    
    # Test connection
    client.admin.command('ping')
    print("MongoDB connection successful!")
    
    # Create/use database
    db = client['tech_prices']
    
    # Test insert
    test_doc = {
        "name": "Connection Test",
        "timestamp": datetime.now(),
        "status": "success"
    }
    
    result = db.test_collection.insert_one(test_doc)
    print(f"Document inserted with ID: {result.inserted_id}")
    
    # Test query
    found = db.test_collection.find_one({"name": "Connection Test"})
    print(f"Document retrieved: {found['name']}")
    
    # Cleanup
    db.test_collection.delete_one({"_id": result.inserted_id})
    print("Test cleanup completed")
    
except Exception as e:
    print(f"Error: {e}")
