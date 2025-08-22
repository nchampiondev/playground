#!/bin/bash
# setup.sh - Project setup script

echo "Setting up Tech Price Scraper..."

# Create project directory structure
echo "Creating directory structure..."
mkdir -p models database scrapers utils tests logs config

# Create __init__.py files
echo "Creating package files..."
touch models/__init__.py
touch database/__init__.py
touch scrapers/__init__.py
touch utils/__init__.py
touch tests/__init__.py
touch config/__init__.py

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Please check your pip installation."
    exit 1
fi

# Test MongoDB connection
echo "Testing MongoDB connection..."
python main.py --test-db

if [ $? -eq 0 ]; then
    echo ""
    echo "Setup completed successfully!"
    echo ""
    echo "Usage:"
    echo "  python main.py           # Run the scraper"
    echo "  python main.py --test-db # Test database connection"
    echo "  python main.py --help    # Show help"
    echo ""
    echo "Project structure created:"
    echo "  models/      # Data models"
    echo "  database/    # MongoDB operations"
    echo "  scrapers/    # Web scraping components"
    echo "  utils/       # Utilities (logging)"
    echo "  tests/       # Unit tests"
    echo "  config/      # Configuration files"
    echo "  logs/        # Log files (auto-created)"
else
    echo "Setup failed! Please check:"
    echo "1. MongoDB is installed and running"
    echo "2. Python dependencies are installed"
    echo "3. All files are in correct locations"
    exit 1
fi

