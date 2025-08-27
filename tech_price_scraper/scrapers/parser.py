import re
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class ProductParser:
    """Parser for extracting product information from HTML"""
    
    def __init__(self):
        self.gpu_keywords = [
            'geforce', 'rtx', 'gtx', 'radeon', 'rx', 'carte graphique',
            'nvidia', 'amd', 'gpu', 'graphics card'
        ]
    
    def parse_topachat_listings(self, html: str, page_url: str) -> List[Dict]:
        """Parse product listings from TopAchat HTML"""
        #logger.info(html)
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        # Try different selectors for product containers
        selectors_to_try = [
            '.product-list__product-wrapper'
        ]

        product_elements = []
        for selector in selectors_to_try:
            product_elements = soup.select(selector)
            if product_elements:
                logger.debug(f"Found {len(product_elements)} products using selector: {selector}")
                break
        
        if not product_elements:
            logger.warning("No products found with standard selectors")
            return products
        
        for element in product_elements:
            try:
                product_data = self._extract_product_data(element, page_url)
                if product_data and self._is_gpu_product(product_data['name']):
                    products.append(product_data)
            except Exception as e:
                logger.warning(f"Error parsing product element: {e}")
                continue
        
        return products
    
    def _extract_product_data(self, element, base_url: str) -> Optional[Dict]:
        """Extract product data from a product element"""
        try:
            # Extract name
            name_elem = element.select_one('.product__label')
            if not name_elem:
                return None
            
            name = name_elem.get_text(strip=True)
            if not name:
                return None
            
            # Extract price
            price_elem = element.select_one('.product__price')
            price = None
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'(\d+[.,]\d+)', price_text)
                if price_match:
                    price = float(price_match.group(1).replace(',', '.'))
            
            # Extract URL
            link_elem = element.select_one('a')
            product_url = ''
            if link_elem and link_elem.get('href'):
                product_url = urljoin(base_url, link_elem.get('href'))
            
            # Extract availability
            availability = self._extract_availability(element)
            
            return {
                'name': name,
                'raw_name': name,
                'price': price,
                'url': product_url,
                'availability': availability
            }
            
        except Exception as e:
            logger.warning(f"Error extracting product data: {e}")
            return None
    
    def _extract_availability(self, element) -> str:
        """Extract availability from product element"""
        availability_elem = element.select_one('.dispo, .stock, .availability')
        if availability_elem:
            avail_text = availability_elem.get_text(strip=True).lower()
            if 'disponible' in avail_text or 'en stock' in avail_text:
                return 'in_stock'
            elif 'rupture' in avail_text or 'épuisé' in avail_text:
                return 'out_of_stock'
            elif 'précommande' in avail_text:
                return 'pre_order'
        
        return 'unknown'
    
    def _is_gpu_product(self, name: str) -> bool:
        """Check if product name indicates it's a GPU"""
        name_lower = name.lower()
        return any(keyword in name_lower for keyword in self.gpu_keywords)
    
    def parse_brand_model(self, name: str) -> tuple:
        """Parse brand and model from product name"""
        name_lower = name.lower()
        
        # Brand detection
        if 'nvidia' in name_lower or 'geforce' in name_lower:
            brand = 'nvidia'
        elif 'amd' in name_lower or 'radeon' in name_lower:
            brand = 'amd'
        elif 'intel' in name_lower:
            brand = 'intel'
        else:
            brand = 'unknown'
        
        # Model extraction
        model_patterns = [
            r'rtx\s*(\d+(?:\s*ti)?(?:\s*super)?)',
            r'gtx\s*(\d+(?:\s*ti)?)',
            r'rx\s*(\d+(?:\s*xt)?)',
            r'(\d{4}(?:\s*xt)?)'
        ]
        
        model = 'unknown'
        for pattern in model_patterns:
            match = re.search(pattern, name_lower)
            if match:
                model = match.group(1).replace(' ', '-')
                break
        
        return brand, model

