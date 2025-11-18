from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.services.twse_service import twse_service
from app.services.finmind_service import finmind_service
from app.crud import crud
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/fetch/revenue")
async def fetch_revenue(
    stock_id: str,
    start_date: str = None,
    end_date: str = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Fetch monthly revenue data from FinMind and store in database.
    """
    logger.info(f"Fetching revenue for {stock_id}")
    
    # Fetch data from FinMind
    revenue_data = await finmind_service.fetch_monthly_revenue(
        stock_id, start_date, end_date
    )
    
    # Store in database
    stored_count = 0
    for item in revenue_data:
        revenue = schemas.MonthlyRevenueCreate(
            stock_id=item["stock_id"],
            revenue_yyyy_mm=item["revenue_yyyy_mm"],
            revenue=item["revenue"],
            revenue_year=item.get("revenue_year"),
            revenue_month=item.get("revenue_month"),
            source=item.get("source")
        )
        crud.upsert_monthly_revenue(db, revenue)
        stored_count += 1
    
    return {
        "stock_id": stock_id,
        "fetched": len(revenue_data),
        "stored": stored_count,
        "message": f"Successfully fetched and stored revenue data for {stock_id}"
    }


@router.post("/fetch/price")
async def fetch_prices(
    stock_ids: List[str],
    db: Session = Depends(get_db)
):
    """
    Fetch current stock prices from TWSE and update cache.
    """
    logger.info(f"Fetching prices for {len(stock_ids)} stocks")
    
    # Fetch data from TWSE
    price_data = await twse_service.fetch_stock_prices(stock_ids)
    
    # Update price cache
    updated_count = 0
    for stock_id, data in price_data.items():
        price_cache = schemas.PriceCacheCreate(
            stock_id=stock_id,
            price=data.get("price"),
            last_close=data.get("last_close"),
            pct=data.get("pct"),
            time_text=data.get("time"),
            source=data.get("source")
        )
        crud.upsert_price_cache(db, price_cache)
        updated_count += 1
    
    return {
        "requested": len(stock_ids),
        "updated": updated_count,
        "message": f"Successfully updated prices for {updated_count} stocks"
    }


@router.post("/fetch/batch-prices")
async def fetch_batch_prices(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Fetch prices for all stocks in watchlist (background task).
    """
    # Get all stocks in watchlist
    watchlist = crud.get_watchlist(db)
    stock_ids = [item.stock_id for item in watchlist]
    
    if not stock_ids:
        return {"message": "No stocks in watchlist", "updated": 0}
    
    logger.info(f"Batch fetching prices for {len(stock_ids)} stocks in watchlist")
    
    # Fetch data from TWSE
    price_data = await twse_service.fetch_stock_prices(stock_ids)
    
    # Update price cache
    updated_count = 0
    for stock_id, data in price_data.items():
        price_cache = schemas.PriceCacheCreate(
            stock_id=stock_id,
            price=data.get("price"),
            last_close=data.get("last_close"),
            pct=data.get("pct"),
            time_text=data.get("time"),
            source=data.get("source")
        )
        crud.upsert_price_cache(db, price_cache)
        updated_count += 1
    
    return {
        "watchlist_size": len(stock_ids),
        "updated": updated_count,
        "message": f"Successfully updated prices for {updated_count}/{len(stock_ids)} stocks"
    }
