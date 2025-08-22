# Tests package
# This package will contain unit tests for the application

# Test configuration
TEST_DATABASE_NAME = "tech_prices_test"
TEST_MONGO_CONNECTION = "mongodb://localhost:27017/"

# Test data samples for future unit tests
SAMPLE_PRODUCT_DATA = {
    "name": "NVIDIA GeForce RTX 4070",
    "price": 599.99,
    "url": "https://example.com/product/123",
    "availability": "in_stock"
}

SAMPLE_HTML_SNIPPET = """
<div class="product-item">
    <h3 class="product-title">NVIDIA GeForce RTX 4070</h3>
    <span class="price">599.99 €</span>
    <span class="availability">En stock</span>
</div>
"""

