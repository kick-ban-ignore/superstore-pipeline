# 🏪 Superstore Sales Pipeline

A minimalistic production-style ELT pipeline built with Python, PostgreSQL and Streamlit.

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Configure environment
- check .env.example & fill in your PostgreSQL credentials

### 3. Run the pipeline
python load_data.py      # Phase 1: Extract & Load
python transform.py      # Phase 2: Transform
streamlit run dashboard.py  # Phase 3: Serve

## Stack
CSV Files -> Python/pandas -> PostgreSQL -> Streamlit Dashboard
- **Python** – Data loading & orchestration
- **PostgreSQL** – Data warehouse
- **SQLAlchemy** – Database connection
- **Streamlit** – Dashboard
- **Plotly** – Charts

## Dashboard
- KPI cards: Total Sales, Profit, Orders, Margin
- Profit by Salesperson
- Profit by Category
- Profit by Person & Category
- Profit Margin % by Person
- Full sortable breakdown table
- Filters: Salesperson, Category, Year, Quarter

Made in Berlin by <a href="https://github.com/kick-ban-ignore" target="_blank" rel="noopener noreferrer">Max</a>, ❤️ and ☕ and some AI for making text more readable 🤖.