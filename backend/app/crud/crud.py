from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
import time
from typing import Optional, List
from datetime import datetime


def get_stock(db: Session, stock_id: str):
    return db.query(models.Stock).filter(models.Stock.stock_id == stock_id).first()


def get_stocks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Stock).offset(skip).limit(limit).all()


def create_stock(db: Session, stock: schemas.StockCreate):
    db_stock = models.Stock(
        stock_id=stock.stock_id,
        name_zh=stock.name_zh,
        created_at=int(time.time()),
        updated_at=int(time.time())
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


def get_watchlist(db: Session):
    return db.query(models.Watchlist).order_by(models.Watchlist.order_index).all()


def get_watchlist_item(db: Session, stock_id: str):
    return db.query(models.Watchlist).filter(models.Watchlist.stock_id == stock_id).first()


def create_watchlist_item(db: Session, watchlist_item: schemas.WatchlistItemCreate):
    db_item = models.Watchlist(
        stock_id=watchlist_item.stock_id,
        is_new=True,
        order_index=0,
        added_at=int(time.time())
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_watchlist_item(db: Session, stock_id: str):
    db_item = db.query(models.Watchlist).filter(models.Watchlist.stock_id == stock_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False


def update_watchlist_item(db: Session, stock_id: str, update_data: schemas.WatchlistItemUpdate):
    db_item = db.query(models.Watchlist).filter(models.Watchlist.stock_id == stock_id).first()
    if db_item:
        if update_data.is_new is not None:
            db_item.is_new = update_data.is_new
        if update_data.order_index is not None:
            db_item.order_index = update_data.order_index
        db.commit()
        db.refresh(db_item)
        return db_item
    return None


def get_monthly_revenues(db: Session, stock_id: str, start: Optional[str] = None, end: Optional[str] = None):
    query = db.query(models.MonthlyRevenue).filter(models.MonthlyRevenue.stock_id == stock_id)
    if start:
        query = query.filter(models.MonthlyRevenue.revenue_yyyy_mm >= start)
    if end:
        query = query.filter(models.MonthlyRevenue.revenue_yyyy_mm <= end)
    return query.order_by(models.MonthlyRevenue.revenue_yyyy_mm.desc()).all()


def create_monthly_revenue(db: Session, revenue: schemas.MonthlyRevenueCreate):
    # Parse year and month from revenue_yyyy_mm
    try:
        parts = revenue.revenue_yyyy_mm.split('-')
        year = int(parts[0])
        month = int(parts[1])
    except:
        year = None
        month = None

    db_revenue = models.MonthlyRevenue(
        stock_id=revenue.stock_id,
        revenue_yyyy_mm=revenue.revenue_yyyy_mm,
        revenue=revenue.revenue,
        revenue_year=year,
        revenue_month=month,
        source=revenue.source,
        updated_at=int(time.time())
    )
    db.add(db_revenue)
    db.commit()
    db.refresh(db_revenue)
    return db_revenue


def upsert_monthly_revenue(db: Session, revenue: schemas.MonthlyRevenueCreate):
    existing = db.query(models.MonthlyRevenue).filter(
        models.MonthlyRevenue.stock_id == revenue.stock_id,
        models.MonthlyRevenue.revenue_yyyy_mm == revenue.revenue_yyyy_mm
    ).first()

    if existing:
        existing.revenue = revenue.revenue
        existing.source = revenue.source
        existing.updated_at = int(time.time())
        db.commit()
        db.refresh(existing)
        return existing
    else:
        return create_monthly_revenue(db, revenue)


def get_price_cache(db: Session, stock_id: str):
    return db.query(models.PriceCache).filter(models.PriceCache.stock_id == stock_id).first()


def upsert_price_cache(db: Session, price_data: schemas.PriceCacheCreate):
    existing = db.query(models.PriceCache).filter(models.PriceCache.stock_id == price_data.stock_id).first()
    
    if existing:
        existing.price = price_data.price
        existing.last_close = price_data.last_close
        existing.pct = price_data.pct
        existing.time_text = price_data.time_text
        existing.source = price_data.source
        existing.fetched_at = int(time.time())
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db_price = models.PriceCache(
            stock_id=price_data.stock_id,
            price=price_data.price,
            last_close=price_data.last_close,
            pct=price_data.pct,
            time_text=price_data.time_text,
            source=price_data.source,
            fetched_at=int(time.time())
        )
        db.add(db_price)
        db.commit()
        db.refresh(db_price)
        return db_price


def get_news_cache(db: Session, stock_id: Optional[str] = None, limit: int = 6):
    query = db.query(models.NewsCache)
    if stock_id:
        query = query.filter(models.NewsCache.stock_id == stock_id)
    return query.order_by(models.NewsCache.fetched_at.desc()).limit(limit).all()
