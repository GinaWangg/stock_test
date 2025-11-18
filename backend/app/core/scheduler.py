"""
Background scheduler for periodic tasks.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.db.database import SessionLocal
from app.services.twse_service import twse_service
from app.crud import crud
from app.schemas import schemas
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def update_watchlist_prices():
    """
    Background job to update prices for all stocks in watchlist.
    Runs every 10 minutes during market hours.
    """
    logger.info("Running scheduled price update for watchlist")
    
    db = SessionLocal()
    try:
        # Get all stocks in watchlist
        watchlist = crud.get_watchlist(db)
        stock_ids = [item.stock_id for item in watchlist]
        
        if not stock_ids:
            logger.info("No stocks in watchlist to update")
            return
        
        # Fetch prices in batches
        batch_size = 50
        total_updated = 0
        
        for i in range(0, len(stock_ids), batch_size):
            batch = stock_ids[i:i + batch_size]
            logger.info(f"Fetching prices for batch {i//batch_size + 1} ({len(batch)} stocks)")
            
            price_data = await twse_service.fetch_stock_prices(batch)
            
            # Update cache
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
                total_updated += 1
        
        logger.info(f"Updated prices for {total_updated}/{len(stock_ids)} stocks")
        
    except Exception as e:
        logger.error(f"Error in scheduled price update: {e}")
    finally:
        db.close()


def start_scheduler():
    """Start the background scheduler."""
    # Update prices every 10 minutes
    scheduler.add_job(
        update_watchlist_prices,
        trigger=IntervalTrigger(minutes=10),
        id="update_prices",
        name="Update watchlist stock prices",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Background scheduler started")


def stop_scheduler():
    """Stop the background scheduler."""
    scheduler.shutdown()
    logger.info("Background scheduler stopped")
