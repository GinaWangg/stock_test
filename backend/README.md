# Stock Revenue Tracking Backend API

FastAPI backend for Taiwan stock revenue observation tool.

## Features

- RESTful API with FastAPI
- SQLite database with WAL mode
- Automatic YoY calculations
- Revenue aggregation (monthly, quarterly)
- Price caching mechanism
- Data fixtures import

## Tech Stack

- Python 3.10+
- FastAPI 0.104+
- SQLAlchemy 2.0+
- Uvicorn (ASGI server)
- Pydantic (validation)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env if needed
```

3. Import initial data:
```bash
python app/scripts/import_fixtures.py
```

4. Run server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. Access API docs:
```
http://localhost:8000/docs
```

## API Endpoints

### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "healthy"
}
```

### Get Watchlist
```http
GET /api/watchlist?sort=prev_month_desc
```

Response:
```json
[
  {
    "stock_id": "2330",
    "name_zh": "台積電",
    "is_new": true,
    "order_index": 0,
    "last_month_revenue": 251466728000,
    "last_month_yoy": 5.18,
    "prev_month_revenue": 251466728000,
    "prev_month_yoy": 14.47,
    "last_quarter_revenue": 741733456000,
    "last_quarter_yoy": null,
    "current_price": {
      "price": null,
      "pct": null,
      "time": null
    }
  }
]
```

### Add to Watchlist
```http
POST /api/watchlist
Content-Type: application/json

{
  "stock_id": "2330"
}
```

Response: 201 Created
```json
{
  "stock_id": "2330",
  "name_zh": "台積電",
  "is_new": true,
  "order_index": 0,
  ...
}
```

### Remove from Watchlist
```http
DELETE /api/watchlist/2330
```

Response: 204 No Content

### Update Watchlist Item
```http
PATCH /api/watchlist/2330
Content-Type: application/json

{
  "is_new": false,
  "order_index": 1
}
```

### Get Stock Detail
```http
GET /api/stocks/2330
```

Response:
```json
{
  "stock_id": "2330",
  "name_zh": "台積電",
  "is_new": true,
  "order_index": 0,
  "last_month_revenue": 251466728000,
  "last_month_yoy": 5.18,
  "prev_month_revenue": 251466728000,
  "prev_month_yoy": 14.47,
  "last_quarter_revenue": 741733456000,
  "last_quarter_yoy": null,
  "monthly_revenues": [
    {
      "revenue_yyyy_mm": "2024-10",
      "revenue": 251466728000,
      "updated_at": 1700000000
    }
  ]
}
```

### Get Monthly Revenue
```http
GET /api/stocks/2330/monthly_revenue?start=2024-01&end=2024-10
```

### Get Prices (Batch)
```http
GET /api/prices?stocks=2330,2317,2454
```

Response:
```json
{
  "2330": {
    "price": null,
    "pct": null,
    "time": null,
    "last_close": null,
    "fetched_at": null,
    "is_stale": true
  },
  "2317": { ... },
  "2454": { ... }
}
```

## Database Schema

### Tables

- **stocks**: Stock master data
- **watchlist**: User tracking list
- **monthly_revenue**: Monthly revenue records
- **price_cache**: Cached stock prices
- **news_cache**: Cached news items
- **ai_analysis_cache**: AI analysis results

### ER Diagram (Simplified)

```
stocks (stock_id, name_zh, ...)
  ├─> watchlist (stock_id, is_new, ...)
  ├─> monthly_revenue (stock_id, revenue_yyyy_mm, revenue, ...)
  ├─> price_cache (stock_id, price, pct, ...)
  └─> news_cache (stock_id, title, url, ...)
```

## Business Logic

### YoY Calculation
```python
YoY = ((current_revenue - previous_year_revenue) / previous_year_revenue) * 100
```

### Quarter Revenue
Sum of 3 consecutive months:
```python
Q1 = Jan + Feb + Mar
Q2 = Apr + May + Jun
Q3 = Jul + Aug + Sep
Q4 = Oct + Nov + Dec
```

### Sorting Options
- `prev_month_desc`: Sort by previous month revenue (descending)
- `custom`: Sort by order_index

## Data Import

The `import_fixtures.py` script imports initial data:

```bash
python app/scripts/import_fixtures.py
```

Imports:
- Stock IDs and names from `fixtures/StockIdMapping.json`
- Monthly revenue data from `fixtures/StockMonthRevenue.json`

## Docker

Build and run:
```bash
docker build -t stock-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data stock-backend
```

## Development

### Project Structure
```
backend/
├── app/
│   ├── api/              # API route handlers
│   │   ├── watchlist.py
│   │   ├── stocks.py
│   │   └── prices.py
│   ├── core/             # Core logic and config
│   │   ├── config.py
│   │   └── business_logic.py
│   ├── crud/             # Database operations
│   │   └── crud.py
│   ├── db/               # Database connection
│   │   └── database.py
│   ├── models/           # SQLAlchemy models
│   │   └── models.py
│   ├── schemas/          # Pydantic schemas
│   │   └── schemas.py
│   ├── scripts/          # Utility scripts
│   │   └── import_fixtures.py
│   └── main.py           # Application entry point
├── fixtures/             # Initial data files
├── data/                 # SQLite database files
├── requirements.txt
└── Dockerfile
```

### Adding New Endpoints

1. Create route handler in `app/api/`
2. Define schemas in `app/schemas/`
3. Add CRUD operations in `app/crud/`
4. Register router in `app/main.py`

### Database Migrations

For production, consider using Alembic:
```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```

## Configuration

Environment variables (`.env`):
```bash
APP_ENV=development
DATABASE_URL=sqlite:///./data/stock_revenue.db
TWSE_API_BASE=https://mis.twse.com.tw/stock/api/getStockInfo.jsp
FINMIND_API_BASE=https://api.finmindtrade.com/api/v4/data
NEWS_API_BASE=https://openapi.twse.com.tw/v1/news/newsList
PRICE_FETCH_BATCH_SIZE=50
PRICE_CACHE_TTL_SECONDS=600
NEWS_CACHE_TTL_SECONDS=300
EXCEL_MAX_ROWS=1000
```

## Testing

Run tests (when implemented):
```bash
pytest tests/
```

## License

MIT
