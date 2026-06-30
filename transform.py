# =============================================================================
# transform.py
# Phase 2: Run SQL transformations against PostgreSQL
# =============================================================================

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

# Order is critical: Staging MUST run before Marts!
SQL_FILES = [
    "sql/staging/stg_orders.sql",
    "sql/marts/mart_sales_performance.sql",
]

def run_sql_file(engine, filepath: str):
    """Reads a .sql file and executes it against the database."""
    print(f"\n⏳ Executing: '{filepath}' ...")

    with open(filepath, "r", encoding="utf-8") as f:
        sql = f.read()

    # Split multiple statements (CREATE VIEW 1, CREATE VIEW 2, ...)
    statements = [s.strip() for s in sql.split(";") if s.strip()]

    with engine.begin() as conn:          # begin() = auto commit & rollback
        for stmt in statements:
            conn.execute(text(stmt))

    print(f"   ✅ '{filepath}' executed successfully!")

def main():
    print("=" * 55)
    print("  🔧 Superstore Pipeline – Phase 2: TRANSFORM")
    print("=" * 55)

    engine = create_engine(DB_URL)

    for sql_file in SQL_FILES:
        try:
            run_sql_file(engine, sql_file)
        except FileNotFoundError:
            print(f"   ❌ File not found: '{sql_file}'")
        except Exception as e:
            print(f"   ❌ Error in '{sql_file}': {e}")
            return  # Stop immediately on error – order matters!

    print("\n" + "=" * 55)
    print("  🏁 Transforms done! Views are live in PostgreSQL.")
    print("=" * 55)

    engine.dispose()

if __name__ == "__main__":
    main()