"""
Data initialization script to import fixtures into database.
"""
import json
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.db.database import SessionLocal, Base, engine
from app.schemas.schemas import StockCreate, MonthlyRevenueCreate
from app.crud import crud


def load_json_file(filepath: str):
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def import_stocks(db, stocks_data):
    """Import stocks from JSON data."""
    print(f"Importing {len(stocks_data)} stocks...")
    for stock_data in stocks_data:
        stock = StockCreate(**stock_data)
        existing = crud.get_stock(db, stock.stock_id)
        if not existing:
            crud.create_stock(db, stock)
            print(f"  Created stock: {stock.stock_id} - {stock.name_zh}")
        else:
            print(f"  Stock already exists: {stock.stock_id}")


def import_monthly_revenue(db, revenue_data):
    """Import monthly revenue from JSON data."""
    print(f"Importing {len(revenue_data)} monthly revenue records...")
    for revenue_item in revenue_data:
        revenue = MonthlyRevenueCreate(**revenue_item)
        crud.upsert_monthly_revenue(db, revenue)
        print(f"  Imported revenue: {revenue.stock_id} - {revenue.revenue_yyyy_mm}")


def main():
    """Main import function."""
    # Create all tables first
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.\n")
    
    db = SessionLocal()
    
    try:
        # Get fixtures directory path
        fixtures_dir = Path(__file__).parent.parent.parent / "fixtures"
        
        # Import stocks
        stocks_file = fixtures_dir / "StockIdMapping.json"
        if stocks_file.exists():
            stocks_data = load_json_file(str(stocks_file))
            import_stocks(db, stocks_data)
        else:
            print(f"Warning: {stocks_file} not found")
        
        # Import monthly revenue
        revenue_file = fixtures_dir / "StockMonthRevenue.json"
        if revenue_file.exists():
            revenue_data = load_json_file(str(revenue_file))
            import_monthly_revenue(db, revenue_data)
        else:
            print(f"Warning: {revenue_file} not found")
        
        print("\nImport completed successfully!")
        
    except Exception as e:
        print(f"Error during import: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
