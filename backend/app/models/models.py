from sqlalchemy import Column, String, Integer, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import time


class Stock(Base):
    __tablename__ = "stocks"

    stock_id = Column(String, primary_key=True)
    name_zh = Column(String, nullable=False)
    created_at = Column(Integer, nullable=False, default=lambda: int(time.time()))
    updated_at = Column(Integer, nullable=False, default=lambda: int(time.time()))

    # Relationships
    watchlist_items = relationship("Watchlist", back_populates="stock")
    monthly_revenues = relationship("MonthlyRevenue", back_populates="stock")
    price_cache = relationship("PriceCache", back_populates="stock", uselist=False)


class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(String, ForeignKey("stocks.stock_id"), nullable=False, unique=True)
    is_new = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
    added_at = Column(Integer, nullable=False, default=lambda: int(time.time()))

    # Relationships
    stock = relationship("Stock", back_populates="watchlist_items")


class MonthlyRevenue(Base):
    __tablename__ = "monthly_revenue"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(String, ForeignKey("stocks.stock_id"), nullable=False)
    revenue_yyyy_mm = Column(String, nullable=False)
    revenue = Column(Integer, nullable=False)
    revenue_year = Column(Integer)
    revenue_month = Column(Integer)
    source = Column(String)
    updated_at = Column(Integer, nullable=False, default=lambda: int(time.time()))

    # Relationships
    stock = relationship("Stock", back_populates="monthly_revenues")

    __table_args__ = (
        {"sqlite_autoincrement": True},
    )


class PriceCache(Base):
    __tablename__ = "price_cache"

    stock_id = Column(String, ForeignKey("stocks.stock_id"), primary_key=True)
    price = Column(Float)
    last_close = Column(Float)
    pct = Column(Float)
    time_text = Column(String)
    fetched_at = Column(Integer, nullable=False, default=lambda: int(time.time()))
    source = Column(String)

    # Relationships
    stock = relationship("Stock", back_populates="price_cache")


class NewsCache(Base):
    __tablename__ = "news_cache"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(String, ForeignKey("stocks.stock_id"), nullable=True)
    title = Column(Text)
    url = Column(Text)
    date_text = Column(String)
    fetched_at = Column(Integer, nullable=False, default=lambda: int(time.time()))


class AIAnalysisCache(Base):
    __tablename__ = "ai_analysis_cache"

    stock_id = Column(String, ForeignKey("stocks.stock_id"), primary_key=True)
    model = Column(String)
    prompt = Column(Text)
    content = Column(Text)
    generated_at = Column(Integer, nullable=False, default=lambda: int(time.time()))
