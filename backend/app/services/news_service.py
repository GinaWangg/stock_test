"""
TWSE News API service for fetching stock news.
"""
import httpx
from typing import List, Dict
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class NewsService:
    """Service for fetching news from TWSE."""
    
    def __init__(self):
        self.base_url = settings.news_api_base
        
    async def fetch_news(self, limit: int = 10) -> List[Dict]:
        """
        Fetch latest news from TWSE.
        
        Args:
            limit: Maximum number of news items to return
            
        Returns:
            List of news items
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.base_url)
                response.raise_for_status()
                data = response.json()
                
                result = []
                if isinstance(data, list):
                    for item in data[:limit]:
                        result.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "date_text": item.get("postDate", ""),
                            "source": "TWSE"
                        })
                
                logger.info(f"Fetched {len(result)} news items from TWSE")
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"Error fetching TWSE news: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching TWSE news: {e}")
            return []


# Singleton instance
news_service = NewsService()
