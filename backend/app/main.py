from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api import watchlist, stocks, prices

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stock Revenue Tracking API",
    description="Backend API for Taiwan Stock Revenue Observation Tool",
    version="1.0.0"
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
