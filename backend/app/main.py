from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import Base, engine
from app.api import watchlist, stocks, prices, fetch, news
from app.core.scheduler import start_scheduler, stop_scheduler
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info("Starting up application...")
    Base.metadata.create_all(bind=engine)
    start_scheduler()
    yield
    # Shutdown
    logger.info("Shutting down application...")
    stop_scheduler()


app = FastAPI(
    title="Stock Revenue Tracking API",
    description="Backend API for Taiwan Stock Revenue Observation Tool",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(watchlist.router, prefix="/api", tags=["watchlist"])
app.include_router(stocks.router, prefix="/api", tags=["stocks"])
app.include_router(prices.router, prefix="/api", tags=["prices"])
app.include_router(fetch.router, prefix="/api", tags=["fetch"])
app.include_router(news.router, prefix="/api", tags=["news"])


@app.get("/")
def read_root():
    return {
        "message": "Stock Revenue Tracking API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
