# =============================================================================
# dashboard.py
# Streamlit Dashboard fed by PostgreSQL
# =============================================================================

import os
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. CONFIGURATION

load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

# Page config
st.set_page_config(
    page_title="Superstore Sales Performance",
    page_icon="🏪",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. DATA LOADING

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_data() -> pd.DataFrame:
    """
    Connects to PostgreSQL and loads the final mart view.
    """
    engine = create_engine(DB_URL)
    df = pd.read_sql("SELECT * FROM mart_sales_performance", engine)
    engine.dispose()
    return df

# -----------------------------------------------------------------------------
# 3. LOAD & VALIDATE

try:
    df = load_data()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()  # Don't render anything if DB is down

# -----------------------------------------------------------------------------
# 4. SIDEBAR – Filters

st.sidebar.image("https://img.icons8.com/fluency/96/shop.png", width=60)
st.sidebar.title("Filters")

# Person filter
all_people = sorted(df["person"].unique().tolist())
selected_people = st.sidebar.multiselect(
    "👤 Salesperson",
    options=all_people,
    default=all_people
)

# Category filter
all_categories = sorted(df["category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "📦 Category",
    options=all_categories,
    default=all_categories
)

# Apply filters
filtered_df = df[
    (df["person"].isin(selected_people)) &
    (df["category"].isin(selected_categories))
]

st.sidebar.markdown("---")
st.sidebar.caption("Data source: PostgreSQL: mart_sales_performance")

# -----------------------------------------------------------------------------
# 5. HEADER

st.title("🏪 Superstore Sales Performance")
st.markdown("**Clean profit analysis**")
st.markdown("---")

# -----------------------------------------------------------------------------
# 6. KPI CARDS – Top row

col1, col2, col3, col4 = st.columns(4)

total_sales    = filtered_df["total_sales"].sum()
total_profit   = filtered_df["total_profit"].sum()
total_orders   = filtered_df["total_orders"].sum()
avg_margin     = (total_profit / total_sales * 100) if total_sales > 0 else 0

col1.metric(
    label="💰 Total Sales",
    value=f"${total_sales:,.0f}"
)
col2.metric(
    label="📈 Total Profit",
    value=f"${total_profit:,.0f}"
)
col3.metric(
    label="🛒 Total Orders",
    value=f"{total_orders:,.0f}"
)
col4.metric(
    label="📊 Profit Margin",
    value=f"{avg_margin:.1f}%"
)

st.markdown("---")

# -----------------------------------------------------------------------------
# 7. CHARTS – Row 1

col_left, col_right = st.columns(2)

# --- Chart 1: Total Profit by Salesperson (Bar Chart)
with col_left:
    st.subheader("🏆 Profit by Salesperson")

    profit_by_person = (
        filtered_df
        .groupby("person")["total_profit"]
        .sum()
        .reset_index()
        .sort_values("total_profit", ascending=True)  # ascending for horizontal bar
    )

    fig_bar = px.bar(
        profit_by_person,
        x="total_profit",
        y="person",
        orientation="h",
        color="total_profit",
        color_continuous_scale="Teal",
        labels={"total_profit": "Total Profit ($)", "person": ""},
        text_auto=",.0f"
    )
    fig_bar.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350
    )
    st.plotly_chart(fig_bar, width=True)

# --- Chart 2: Profit Split by Category (Donut Chart)
with col_right:
    st.subheader("🍩 Profit by Category")

    profit_by_cat = (
        filtered_df
        .groupby("category")["total_profit"]
        .sum()
        .reset_index()
    )

    fig_donut = px.pie(
        profit_by_cat,
        values="total_profit",
        names="category",
        hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_donut.update_traces(
        textposition="outside",
        textinfo="percent+label"
    )
    fig_donut.update_layout(
        showlegend=False,
        height=350,
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_donut, width=True)

# -----------------------------------------------------------------------------
# 8. CHARTS – Row 2

col_left2, col_right2 = st.columns(2)

# --- Chart 3: Profit by Person AND Category (Grouped Bar)
with col_left2:
    st.subheader("📊 Profit by Person & Category")

    fig_grouped = px.bar(
        filtered_df.sort_values("total_profit", ascending=False),
        x="person",
        y="total_profit",
        color="category",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"total_profit": "Total Profit ($)", "person": ""}
    )
    fig_grouped.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
        legend_title="Category"
    )
    st.plotly_chart(fig_grouped, width=True)

# --- Chart 4: Profit Margin % by Person (Bar Chart)
with col_right2:
    st.subheader("📉 Profit Margin % by Person")

    margin_by_person = (
        filtered_df
        .groupby("person")
        .apply(lambda x: (x["total_profit"].sum() / x["total_sales"].sum() * 100)
               if x["total_sales"].sum() > 0 else 0)
        .reset_index()
        .rename(columns={0: "profit_margin_pct"})
        .sort_values("profit_margin_pct", ascending=True)
    )

    fig_margin = px.bar(
        margin_by_person,
        x="profit_margin_pct",
        y="person",
        orientation="h",
        color="profit_margin_pct",
        color_continuous_scale="RdYlGn",
        labels={"profit_margin_pct": "Profit Margin (%)", "person": ""},
        text_auto=".1f"
    )
    fig_margin.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350
    )
    st.plotly_chart(fig_margin, width='stretch')
    
# -----------------------------------------------------------------------------
# 9. DETAILED TABLE

st.markdown("---")
st.subheader("📋 Full Breakdown")

# Format the numbers nicely before displaying
display_df = filtered_df.copy()
display_df["total_sales"]         = display_df["total_sales"].map("${:,.2f}".format)
display_df["total_profit"]        = display_df["total_profit"].map("${:,.2f}".format)
display_df["total_shipping_cost"] = display_df["total_shipping_cost"].map("${:,.2f}".format)
display_df["avg_discount_pct"]    = display_df["avg_discount_pct"].map("{:.1f}%".format)
display_df["profit_margin_pct"]   = display_df["profit_margin_pct"].map("{:.2f}%".format)

display_df.columns = [
    "Person", "Category", "Total Orders", "Total Quantity",
    "Total Sales", "Total Profit", "Total Shipping Cost",
    "Avg Discount %", "Profit Margin %"
]

st.dataframe(display_df, width=True, hide_index=True)