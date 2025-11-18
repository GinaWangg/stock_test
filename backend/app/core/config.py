from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///./data/stock_revenue.db"
    twse_api_base: str = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
    finmind_api_base: str = "https://api.finmindtrade.com/api/v4/data"
    news_api_base: str = "https://openapi.twse.com.tw/v1/news/newsList"
    price_fetch_batch_size: int = 50
    price_cache_ttl_seconds: int = 600
    news_cache_ttl_seconds: int = 300
    excel_max_rows: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
