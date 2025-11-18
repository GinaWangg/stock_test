from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import schemas
from app.crud import crud
from app.core.business_logic import build_watchlist_item_response
from app.services.finmind_service import finmind_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


async def fetch_stock_data_background(stock_id: str):
    """Background task to fetch revenue data for newly added stock."""
    from app.db.database import SessionLocal
    
    db = SessionLocal()
    try:
        logger.info(f"Background fetch: Getting revenue data for {stock_id}")
        
        # Fetch revenue data from FinMind
        revenue_data = await finmind_service.fetch_monthly_revenue(stock_id)
        
        # Store in database
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
        
        logger.info(f"Background fetch: Stored {len(revenue_data)} revenue records for {stock_id}")
        
    except Exception as e:
        logger.error(f"Background fetch error for {stock_id}: {e}")
    finally:
        db.close()


@router.get("/watchlist", response_model=List[dict])
def get_watchlist(
    sort: str = "prev_month_desc",
    db: Session = Depends(get_db)
):
    """
    Get complete watchlist with all calculated fields.
    Query params:
        - sort: 'prev_month_desc' | 'custom' (default: prev_month_desc)
    """
    watchlist_items = crud.get_watchlist(db)
    
    results = []
    for item in watchlist_items:
        response_item = build_watchlist_item_response(db, item)
        if response_item:
            results.append(response_item)
    
    # Apply sorting
    if sort == "prev_month_desc":
        results.sort(
            key=lambda x: x.get("prev_month_revenue") or 0,
            reverse=True
        )
    elif sort == "custom":
        results.sort(key=lambda x: x.get("order_index", 0))
    
    return results


@router.post("/watchlist", status_code=201)
async def add_to_watchlist(
    watchlist_item: schemas.WatchlistItemCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Add a stock to watchlist.
    If stock doesn't exist in stocks table, it needs to be created first.
    Background task will fetch revenue and price data.
    """
    # Check if already in watchlist
    existing = crud.get_watchlist_item(db, watchlist_item.stock_id)
    if existing:
        raise HTTPException(status_code=400, detail="Stock already in watchlist")
    
    # Check if stock exists, if not return error
    # In real implementation, we'd look up from a master list or create with name
    stock = crud.get_stock(db, watchlist_item.stock_id)
    if not stock:
        # For now, raise error - in production we'd auto-create or lookup
        raise HTTPException(
            status_code=404,
            detail=f"Stock {watchlist_item.stock_id} not found. Please ensure stock exists in database."
        )
    
    # Create watchlist item
    db_item = crud.create_watchlist_item(db, watchlist_item)
    
    # Add background task to fetch revenue data
    background_tasks.add_task(fetch_stock_data_background, watchlist_item.stock_id)
    logger.info(f"Added background task to fetch data for {watchlist_item.stock_id}")
    
    # Return current state (might have empty fields until background task completes)
    response = build_watchlist_item_response(db, db_item)
    return response


@router.delete("/watchlist/{stock_id}", status_code=204)
def remove_from_watchlist(
    stock_id: str,
    db: Session = Depends(get_db)
):
    """Remove a stock from watchlist."""
    success = crud.delete_watchlist_item(db, stock_id)
    if not success:
        raise HTTPException(status_code=404, detail="Stock not found in watchlist")
    return None


@router.patch("/watchlist/{stock_id}")
def update_watchlist_item(
    stock_id: str,
    update_data: schemas.WatchlistItemUpdate,
    db: Session = Depends(get_db)
):
    """Update watchlist item fields (is_new, order_index)."""
    updated_item = crud.update_watchlist_item(db, stock_id, update_data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Stock not found in watchlist")
    
    response = build_watchlist_item_response(db, updated_item)
    return response
