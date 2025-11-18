from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.database import get_db
from app.schemas import schemas
from app.crud import crud
from app.core.business_logic import build_watchlist_item_response

router = APIRouter()


@router.get("/stocks/{stock_id}")
def get_stock_detail(
    stock_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed information for a single stock."""
    stock = crud.get_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    # Get all monthly revenues
    revenues = crud.get_monthly_revenues(db, stock_id)
    
    # Get price cache
    price_cache = crud.get_price_cache(db, stock_id)
    
    # Build similar response to watchlist item
    # Check if in watchlist
    watchlist_item = crud.get_watchlist_item(db, stock_id)
    
    if watchlist_item:
        response = build_watchlist_item_response(db, watchlist_item)
    else:
        # Build minimal response for non-watchlist stock
        response = {
            "stock_id": stock.stock_id,
            "name_zh": stock.name_zh,
            "is_new": False,
            "order_index": 0,
        }
    
    # Add monthly revenues list
    response["monthly_revenues"] = [
        {
            "revenue_yyyy_mm": r.revenue_yyyy_mm,
            "revenue": r.revenue,
            "updated_at": r.updated_at
        }
        for r in revenues[:24]  # Last 24 months
    ]
    
    return response


@router.get("/stocks/{stock_id}/monthly_revenue")
def get_stock_monthly_revenue(
    stock_id: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get monthly revenue series for a stock."""
    stock = crud.get_stock(db, stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    revenues = crud.get_monthly_revenues(db, stock_id, start, end)
    
    return [
        {
            "revenue_yyyy_mm": r.revenue_yyyy_mm,
            "revenue": r.revenue,
            "revenue_year": r.revenue_year,
            "revenue_month": r.revenue_month,
            "updated_at": r.updated_at
        }
        for r in revenues
    ]
