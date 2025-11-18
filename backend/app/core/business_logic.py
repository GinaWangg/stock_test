from sqlalchemy.orm import Session
from app.crud import crud
from typing import List, Optional, Dict
from datetime import datetime
import time


def calculate_yoy(current_value: Optional[int], previous_value: Optional[int]) -> Optional[float]:
    """Calculate Year-over-Year percentage change."""
    if current_value is None or previous_value is None or previous_value == 0:
        return None
    return round(((current_value - previous_value) / previous_value) * 100, 2)


def get_last_n_months_revenue(revenues: List, n: int = 1):
    """Get revenue from n months ago (1 = last month, 2 = month before last)."""
    if len(revenues) >= n:
        return revenues[n - 1]
    return None


def calculate_quarter_revenue(revenues: List, start_idx: int = 0) -> Optional[int]:
    """Calculate sum of 3 consecutive months starting from start_idx."""
    if len(revenues) < start_idx + 3:
        return None
    return sum(r.revenue for r in revenues[start_idx:start_idx + 3])


def get_revenue_from_year_ago(revenues: List, current_month_data) -> Optional[int]:
    """Find revenue from same month last year."""
    if not current_month_data:
        return None
    
    current_year = current_month_data.revenue_year
    current_month = current_month_data.revenue_month
    
    if current_year is None or current_month is None:
        return None
    
    target_year = current_year - 1
    for rev in revenues:
        if rev.revenue_year == target_year and rev.revenue_month == current_month:
            return rev.revenue
    
    return None


def build_watchlist_item_response(db: Session, watchlist_db_item) -> Dict:
    """Build complete watchlist item response with all calculated fields."""
    stock = crud.get_stock(db, watchlist_db_item.stock_id)
    if not stock:
        return None
    
    # Get monthly revenues (sorted by date desc)
    revenues = crud.get_monthly_revenues(db, watchlist_db_item.stock_id)
    
    # Initialize response
    response = {
        "stock_id": watchlist_db_item.stock_id,
        "name_zh": stock.name_zh,
        "is_new": watchlist_db_item.is_new,
        "order_index": watchlist_db_item.order_index,
        "last_month_revenue": None,
        "last_month_yoy": None,
        "prev_month_revenue": None,
        "prev_month_yoy": None,
        "last_quarter_revenue": None,
        "last_quarter_yoy": None,
        "current_price": None
    }
    
    # Calculate last month
    last_month = get_last_n_months_revenue(revenues, 1)
    if last_month:
        response["last_month_revenue"] = last_month.revenue
        last_month_prev_year = get_revenue_from_year_ago(revenues, last_month)
        response["last_month_yoy"] = calculate_yoy(last_month.revenue, last_month_prev_year)
    
    # Calculate previous month
    prev_month = get_last_n_months_revenue(revenues, 2)
    if prev_month:
        response["prev_month_revenue"] = prev_month.revenue
        prev_month_prev_year = get_revenue_from_year_ago(revenues, prev_month)
        response["prev_month_yoy"] = calculate_yoy(prev_month.revenue, prev_month_prev_year)
    
    # Calculate last quarter (most recent complete 3 months)
    last_quarter = calculate_quarter_revenue(revenues, 0)
    if last_quarter:
        response["last_quarter_revenue"] = last_quarter
        # Calculate YoY for quarter (compare with same quarter last year)
        prev_year_quarter = calculate_quarter_revenue(revenues, 12)  # 12 months ago
        response["last_quarter_yoy"] = calculate_yoy(last_quarter, prev_year_quarter)
    
    # Get current price
    price_cache = crud.get_price_cache(db, watchlist_db_item.stock_id)
    if price_cache:
        response["current_price"] = {
            "price": price_cache.price,
            "pct": price_cache.pct,
            "time": price_cache.time_text
        }
    
    return response
