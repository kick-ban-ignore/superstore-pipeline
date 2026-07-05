# 🏪 Superstore Sales Pipeline

A minimalistic production-style ELT pipeline built with Python, PostgreSQL and Streamlit.

## Architecture
CSV Files -> Python/pandas -> PostgreSQL -> Streamlit Dashboard

## Stack
- **Python** – Data loading & orchestration
- **PostgreSQL** – Data warehouse
- **SQLAlchemy** – Database connection
- **Streamlit** – Dashboard
- **Plotly** – Charts

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Configure environment
cp .env.example .env
# Fill in your PostgreSQL credentials

### 3. Run the pipeline
python load_data.py      # Phase 1: Load
python transform.py      # Phase 2: Transform
streamlit run dashboard.py  # Phase 3: Serve

## Dashboard
- KPI cards: Total Sales, Profit, Orders, Margin
- Profit by Salesperson
- Profit by Category
- Profit by Person & Category
- Profit Margin % by Person
- Full sortable breakdown table
- Filters: Salesperson, Category, Year, Quarter