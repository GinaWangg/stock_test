"""
FinMind API service for fetching monthly revenue data.
"""
import httpx
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class FinMindService:
    """Service for interacting with FinMind API."""
    
    def __init__(self):
        self.base_url = settings.finmind_api_base
        
    async def fetch_monthly_revenue(
        self,
        stock_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch monthly revenue data from FinMind.
        
        Args:
            stock_id: Stock ID (e.g., '2330')
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of revenue records
        """
        # Default to last 24 months if not specified
        if not start_date:
            start = datetime.now() - timedelta(days=730)  # ~24 months
            start_date = start.strftime("%Y-%m-%d")
        
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    self.base_url,
                    params={
                        "dataset": "TaiwanStockMonthRevenue",
                        "data_id": stock_id,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                result = []
                if "data" in data and isinstance(data["data"], list):
                    for item in data["data"]:
                        # FinMind returns: date, stock_id, revenue, etc.
                        date_str = item.get("date", "")
                        revenue = item.get("revenue", 0)
                        
                        # Convert revenue from thousand NTD to NTD
                        revenue_ntd = int(revenue * 1000) if revenue else 0
                        
                        # Parse date to get year and month
                        try:
                            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                            revenue_yyyy_mm = f"{date_obj.year}-{date_obj.month}"
                            revenue_year = date_obj.year
                            revenue_month = date_obj.month
                        except ValueError:
                            logger.warning(f"Invalid date format: {date_str}")
                            continue
                        
                        result.append({
                            "stock_id": stock_id,
                            "revenue_yyyy_mm": revenue_yyyy_mm,
                            "revenue": revenue_ntd,
                            "revenue_year": revenue_year,
                            "revenue_month": revenue_month,
                            "source": "FinMind"
                        })
                
                logger.info(f"Fetched {len(result)} revenue records for {stock_id} from FinMind")
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"Error fetching FinMind data for {stock_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching FinMind data for {stock_id}: {e}")
            return []


# Singleton instance
finmind_service = FinMindService()
