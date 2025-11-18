from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.news_service import news_service
from app.crud import crud
from app.models import models
import time

router = APIRouter()


@router.get("/news")
async def get_news(
    limit: int = 6,
    db: Session = Depends(get_db)
):
    """
    Get latest news, with caching.
    """
    # Check cache first
    cached_news = crud.get_news_cache(db, stock_id=None, limit=limit)
    
    # If cache is fresh (less than 5 minutes old), return it
    current_time = int(time.time())
    if cached_news and (current_time - cached_news[0].fetched_at) < 300:
        return [
            {
                "id": news.id,
                "title": news.title,
                "url": news.url,
                "date_text": news.date_text,
                "fetched_at": news.fetched_at
            }
            for news in cached_news
        ]
    
    # Fetch fresh news
    news_items = await news_service.fetch_news(limit=limit)
    
    # Clear old cache and store new
    db.query(models.NewsCache).filter(models.NewsCache.stock_id.is_(None)).delete()
    
    for item in news_items:
        news_cache = models.NewsCache(
            stock_id=None,
            title=item["title"],
            url=item["url"],
            date_text=item["date_text"],
            fetched_at=current_time
        )
        db.add(news_cache)
    
    db.commit()
    
    return news_items


@router.get("/stocks/{stock_id}/news")
async def get_stock_news(
    stock_id: str,
    limit: int = 6,
    db: Session = Depends(get_db)
):
    """
    Get news for a specific stock (cached).
    """
    cached_news = crud.get_news_cache(db, stock_id=stock_id, limit=limit)
    
    return [
        {
            "id": news.id,
            "title": news.title,
            "url": news.url,
            "date_text": news.date_text,
            "fetched_at": news.fetched_at
        }
        for news in cached_news
    ]
