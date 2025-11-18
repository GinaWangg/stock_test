"""
TWSE API service for fetching stock prices and data.
"""
import httpx
from typing import List, Dict, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class TWSEService:
    """Service for interacting with TWSE API."""
    
    def __init__(self):
        self.base_url = settings.twse_api_base
        
    async def fetch_stock_prices(self, stock_ids: List[str]) -> Dict[str, Dict]:
        """
        Fetch stock prices from TWSE API.
        
        Args:
            stock_ids: List of stock IDs (e.g., ['2330', '2317'])
            
        Returns:
            Dictionary mapping stock_id to price data
        """
        result = {}
        
        # TWSE API format: ex_ch=tse_2330.tw|tse_2317.tw
        ex_ch = "|".join([f"tse_{sid}.tw" for sid in stock_ids])
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    self.base_url,
                    params={"ex_ch": ex_ch, "json": "1"}
                )
                response.raise_for_status()
                data = response.json()
                
                if "msgArray" in data:
                    for item in data["msgArray"]:
                        stock_id = item.get("c", "").replace(".tw", "")
                        if stock_id:
                            result[stock_id] = {
                                "price": self._parse_float(item.get("z")),  # 成交價
                                "last_close": self._parse_float(item.get("y")),  # 昨收
                                "pct": self._calculate_pct(
                                    item.get("z"),
                                    item.get("y")
                                ),
                                "time": item.get("t"),  # 時間
                                "volume": self._parse_float(item.get("v")),  # 成交量
                                "source": "TWSE"
                            }
                
                logger.info(f"Fetched prices for {len(result)} stocks from TWSE")
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"Error fetching TWSE data: {e}")
            return result
        except Exception as e:
            logger.error(f"Unexpected error fetching TWSE data: {e}")
            return result
    
    def _parse_float(self, value: Optional[str]) -> Optional[float]:
        """Parse string to float, handling '-' and None."""
        if value is None or value == "-":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _calculate_pct(self, current: Optional[str], previous: Optional[str]) -> Optional[float]:
        """Calculate percentage change."""
        current_f = self._parse_float(current)
        previous_f = self._parse_float(previous)
        
        if current_f is None or previous_f is None or previous_f == 0:
            return None
        
        return round(((current_f - previous_f) / previous_f) * 100, 2)


# Singleton instance
twse_service = TWSEService()
