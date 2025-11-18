from pydantic import BaseModel
from typing import Optional


class StockBase(BaseModel):
    stock_id: str
    name_zh: str


class StockCreate(StockBase):
    pass


class Stock(StockBase):
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class WatchlistItemBase(BaseModel):
    stock_id: str


class WatchlistItemCreate(WatchlistItemBase):
    pass


class WatchlistItemUpdate(BaseModel):
    is_new: Optional[bool] = None
    order_index: Optional[int] = None


class CurrentPrice(BaseModel):
    price: Optional[float]
    pct: Optional[float]
    time: Optional[str]


class WatchlistItem(BaseModel):
    stock_id: str
    name_zh: str
    is_new: bool
    order_index: int
    last_month_revenue: Optional[int]
    last_month_yoy: Optional[float]
    prev_month_revenue: Optional[int]
    prev_month_yoy: Optional[float]
    last_quarter_revenue: Optional[int]
    last_quarter_yoy: Optional[float]
    current_price: Optional[CurrentPrice]

    class Config:
        from_attributes = True


class MonthlyRevenueBase(BaseModel):
    stock_id: str
    revenue_yyyy_mm: str
    revenue: int


class MonthlyRevenueCreate(MonthlyRevenueBase):
    revenue_year: Optional[int] = None
    revenue_month: Optional[int] = None
    source: Optional[str] = None


class MonthlyRevenue(MonthlyRevenueBase):
    id: int
    revenue_year: Optional[int]
    revenue_month: Optional[int]
    source: Optional[str]
    updated_at: int

    class Config:
        from_attributes = True


class PriceCacheBase(BaseModel):
    stock_id: str
    price: Optional[float]
    last_close: Optional[float]
    pct: Optional[float]
    time_text: Optional[str]
    source: Optional[str]


class PriceCacheCreate(PriceCacheBase):
    pass


class PriceCache(PriceCacheBase):
    fetched_at: int

    class Config:
        from_attributes = True


class NewsItem(BaseModel):
    id: int
    stock_id: Optional[str]
    title: Optional[str]
    url: Optional[str]
    date_text: Optional[str]
    fetched_at: int

    class Config:
        from_attributes = True
