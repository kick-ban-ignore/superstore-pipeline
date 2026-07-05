# 🏪 Superstore Sales Pipeline

A minimalistic production-style ELT pipeline built with Python, PostgreSQL and Streamlit.

## How to Run
### Running Locally. 
- dashboard.py requires a local PostgreSQL instance. See .env.example for configuration.

### Running online. 
- dashboard_online.py does not need a database and reads directly from a csv. You can see it live here:  https://superstore-pipelinegit-hcueiwmlwn7tarjtfmftgk.streamlit.app/

### 1. Install dependencies
- pip install -r requirements.txt

### 2. Configure environment
- Check .env.example & fill in your PostgreSQL credentials

### 3. Run the pipeline
- python load_data.py      # Phase 1: Extract & Load
- python transform.py      # Phase 2: Transform
- streamlit run dashboard.py  # Phase 3: Serve

## Stack
CSV Files -> Python/pandas -> PostgreSQL -> Streamlit Dashboard
- **Python** – Data loading & orchestration
- **PostgreSQL** – Data warehouse
- **SQLAlchemy** – Database connection
- **Streamlit** – Dashboard
- **Plotly** – Charts

## Dashboard
<img width="1920" height="919" alt="Screenshot 2026-07-05 at 19-14-03 🛒 Superstore Sales Performance" src="https://github.com/user-attachments/assets/11b3b73b-05d6-4926-b22f-ed7413a9ca9d" />

- KPI cards: Total Sales, Profit, Orders, Margin
- Profit by Salesperson
- Profit by Category
- Profit by Person & Category
- Profit Margin % by Person
- Full sortable breakdown table
- Filters: Salesperson, Category, Year, Quarter
<img width="1445" height="507" alt="Screenshot 2026-07-05 at 19-14-18 🛒 Superstore Sales Performance" src="https://github.com/user-attachments/assets/9461fbb0-e506-4bbc-a7e5-0251bc362c10" />


Made in Berlin by <a href="https://github.com/kick-ban-ignore" target="_blank" rel="noopener noreferrer">Max</a>, ❤️ and ☕ and some AI for making text more readable 🤖.
