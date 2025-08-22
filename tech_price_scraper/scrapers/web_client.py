import requests
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class WebClient:
    """HTTP client for web scraping with rate limiting and error handling"""
    
    def __init__(self, rate_limit_ms: int = 1000, max_retries: int = 3):
        self.session = requests.Session()
        self.rate_limit_ms = rate_limit_ms
        self.max_retries = max_retries
        self.last_request_time = 0
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        """Make GET request with rate limiting and retries"""
        for attempt in range(self.max_retries):
            try:
                # Apply rate limiting
                self._apply_rate_limit()
                
                response = self.session.get(url, timeout=10, **kwargs)
                response.raise_for_status()
                
                logger.debug(f"Successfully fetched: {url}")
                return response
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {url} - {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All retries failed for: {url}")
                    return None
        
        return None
    
    def _apply_rate_limit(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        time_since_last = (current_time - self.last_request_time) * 1000
        
        if time_since_last < self.rate_limit_ms:
            sleep_time = (self.rate_limit_ms - time_since_last) / 1000
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def close(self):
        """Close the session"""
        self.session.close()

