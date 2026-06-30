# =============================================================================
# load_data.py
# Extract & Load CSVs as raw tables into PostgreSQL
# =============================================================================

import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. CONFIGURATION

# Load pw via .env
load_dotenv()

# Building a Connection String
DB_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

# Mapping: table name in PostgreSQL references path in CSV

CSV_TABLE_MAP = {
    "raw_orders":          "data/orders.csv",
    "raw_products":        "data/products.csv",
    "raw_people":          "data/people.csv",
    "raw_returned_orders": "data/returned_orders.csv",
}

# -----------------------------------------------------------------------------
# 2. BUILD ENGINE

def get_engine():
    """Creates SQLAlchemy Engine."""
    engine = create_engine(DB_URL)
    # Test connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Connection to PostgreSQL successful!")
    return engine

# -----------------------------------------------------------------------------
# 3. LOAD

def load_csv_to_postgres(engine, table_name: str, csv_path: str):
    """
    Reads a CSV file and writes it 1:1 as a raw table in PostgreSQL.
    
    Args:
        engine:     SQLAlchemy Engine
        table_name: name of target table in PostgreSQL
        csv_path:   Relative path to the CSV file
    """
    print(f"\n Loading '{csv_path}' to table '{table_name}' ...")
    
    # Read in CSV with Pandas
    df = pd.read_csv(csv_path)
    
    # Clean up column names: Remove leading/trailing whitespace and replace special characters
    # "Order Date" to "order_date", PostgreSQL-friendly
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    # Remove unnamed or index columns
    df = df.loc[:, ~df.columns.str.match(r'^(unnamed.*|index)$')]
    
    print(f"   {len(df):,} Rows | {len(df.columns)} Columns found")
    print(f"    Columns: {list(df.columns)}")
    
    # Write to PostgreSQL
    # if_exists='replace' - Table will be rebuilt on every run (idempotent!)
    # index=False - Pandas Index NOT written as a column
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",  # Clean reload – no duplicate data
        index=False
    )
    
    print(f"   '{table_name}' successfully loaded!")

# -----------------------------------------------------------------------------
# 4. MAIN – Orchestration
# -----------------------------------------------------------------------------

def main():
    print("=" * 55)
    print("Superstore Pipeline - LOAD")
    print("=" * 55)
    
    # Start Engine 1x
    try:
        engine = get_engine()
    except Exception as e:
        print(f"Connection error: {e}")
        print("Is PostgreSQL running? Do the .env credentials match?")
        return
    
    # Load all CSVs
    success_count = 0
    for table_name, csv_path in CSV_TABLE_MAP.items():
        try:
            load_csv_to_postgres(engine, table_name, csv_path)
            success_count += 1
        except FileNotFoundError:
            print(f"File not found: '{csv_path}' – skipped.")
        except SQLAlchemyError as e:
            print(f"Database error for '{table_name}': {e}")
    
    # Completion Report
    print("\n" + "=" * 55)
    print(f"Finished! {success_count}/{len(CSV_TABLE_MAP)} tables loaded.")
    print("=" * 55)
    
    # Dispose Engine cleanly
    engine.dispose()

if __name__ == "__main__":
    main()