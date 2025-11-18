from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.crud import crud
import time
from app.core.config import settings

router = APIRouter()


@router.get("/prices")
def get_prices(
    stocks: str = Query(..., description="Comma-separated stock IDs"),
    db: Session = Depends(get_db)
):
    """
    Get cached prices for multiple stocks.
    If cache is stale (> TTL), return cached data but could trigger background refresh.
    """
    stock_ids = [s.strip() for s in stocks.split(",") if s.strip()]
    
    results = {}
    current_time = int(time.time())
    
    for stock_id in stock_ids:
        price_cache = crud.get_price_cache(db, stock_id)
        
        if price_cache:
            is_stale = (current_time - price_cache.fetched_at) > settings.price_cache_ttl_seconds
            
            results[stock_id] = {
                "price": price_cache.price,
                "pct": price_cache.pct,
                "time": price_cache.time_text,
                "last_close": price_cache.last_close,
                "fetched_at": price_cache.fetched_at,
                "is_stale": is_stale
            }
        else:
            results[stock_id] = {
                "price": None,
                "pct": None,
                "time": None,
                "last_close": None,
                "fetched_at": None,
                "is_stale": True
            }
    
    return results
