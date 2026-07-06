# =============================================================================
# dashboard.py
# Streamlit Dashboard fed by CSV file
# =============================================================================

import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. CONFIGURATION

# Page config
st.set_page_config(
    page_title="🛒 Superstore Sales Performance",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. DATA LOADING

@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv("data/mart_sales_performance.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ data/mart_sales_performance.csv not found!")
    st.stop()

# -----------------------------------------------------------------------------
# 4. SIDEBAR – Filters

st.sidebar.image("https://img.icons8.com/fluency/96/shop.png", width=60)
st.sidebar.title("Filters")

# Person filter
all_people = sorted(df["person"].unique().tolist())
selected_people = st.sidebar.multiselect(
    "Salesperson",
    options=all_people,
    default=all_people
)

# Category filter
all_categories = sorted(df["category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Category",
    options=all_categories,
    default=all_categories
)

# Time filter
st.sidebar.markdown("---")
st.sidebar.subheader("Time Period")

# Dynamically pull available years from the data – no hardcoding!
all_years = sorted(df["order_year"].astype(int).unique().tolist(), reverse=True)

selected_years = st.sidebar.multiselect(
    "Year",
    options=all_years,
    default=all_years
)

# Quarter selector with friendly labels
quarter_labels = {1: "Q1 (Jan–Mar)", 2: "Q2 (Apr–Jun)",
                  3: "Q3 (Jul–Sep)", 4: "Q4 (Oct–Dec)"}

selected_quarters = st.sidebar.multiselect(
    "Quarter",
    options=list(quarter_labels.keys()),
    default=list(quarter_labels.keys()),
    format_func=lambda x: quarter_labels[x]  # Show "Q1 (Jan-Mar)" instead of "1"
)

# Apply filters
filtered_df = df[
    (df["person"].isin(selected_people))                     &
    (df["category"].isin(selected_categories))               &
    (df["order_year"].astype(int).isin(selected_years))      &
    (df["order_quarter"].astype(int).isin(selected_quarters))
]

st.sidebar.markdown("---")
st.sidebar.caption("Data source:")
st.sidebar.caption("Table: mart_sales_performance.csv")
current_time = datetime.now().strftime("%H:%M:%S")
st.sidebar.caption("Loaded at: " + current_time )

st.sidebar.markdown(
    'Made in Berlin by <a href="https://github.com/kick-ban-ignore" target="_blank" rel="noopener noreferrer">Max</a>, ❤️ and ☕',
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 5. HEADER

st.title("Superstore Sales Performance")
st.markdown("**Sales, profit, orders**")

# Show active time period
year_str    = ", ".join(str(y) for y in sorted(selected_years))
quarter_str = ", ".join(quarter_labels[q] for q in sorted(selected_quarters))

# Guard in case of empty selection
if filtered_df.empty:
    st.warning("⚠️ No data for the selected filters. Try adjusting your selection.")
    st.stop()

st.caption(f"Showing: {year_str}  ·  {quarter_str}")

st.markdown("---")


# -----------------------------------------------------------------------------
# 6. KPI CARDS – Top row

col1, col2, col3, col4 = st.columns(4)

total_sales  = filtered_df["total_sales"].sum()
total_profit = filtered_df["total_profit"].sum()
total_orders = filtered_df["total_orders"].sum()
avg_margin   = (total_profit / total_sales * 100) ## if total_sales > 0 else 0

# European format helper
# . for thousands separator, , for decimal separator
def eu_currency(value):
    return f"${value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

def eu_number(value):
    return f"{value:,.0f}".replace(",", ".")

col1.metric("Total Sales",   eu_currency(total_sales))
col2.metric("Total Profit",  eu_currency(total_profit))
col3.metric("Total Orders",  eu_number(total_orders))
col4.metric("Profit Margin", f"{avg_margin:.1f}%".replace(".", ","))

st.markdown("---")

# -----------------------------------------------------------------------------
# 7. CHARTS – Row 1

col_left, col_right = st.columns(2)

# --- Chart 1: Total Profit by Salesperson (Bar Chart)
with col_left:
    st.subheader("Profit by Salesperson")

    profit_by_person = (
        filtered_df
        .groupby("person")["total_profit"]
        .sum()
        .reset_index()
        .sort_values("total_profit", ascending=False)
    )

    fig_bar = px.bar(
        profit_by_person,
        x="person",
        y="total_profit",
        color="total_profit",
        color_continuous_scale="Teal",
        labels={"total_profit": "Total Profit ($)", "person": ""},
        text_auto=",.0f"
    )
    fig_bar.update_layout(
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=450,
        xaxis_tickangle=-35,         # Angled labels so names don't overlap
        margin=dict(l=20, r=20, t=20, b=120)  # Bottom margin for names
    )
    fig_bar.update_traces(
        textposition="outside",
        textangle=0
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Chart 2: Profit Split by Category (Donut Chart)
with col_right:
    st.subheader("Profit by Category")

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
        color_discrete_sequence=px.colors.qualitative.Pastel   
    )
    fig_donut.update_traces(
        textposition="inside",       
        insidetextorientation="radial"
    )
    fig_donut.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=60)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# -----------------------------------------------------------------------------
# 8. CHARTS – Row 2

col_left2, col_right2 = st.columns(2)

# --- Chart 3: Profit by Person AND Category (Grouped Bar)
with col_left2:
    st.subheader("Profit by Person & Category")

    person_cat_df = (
        filtered_df
        .groupby(["person", "category"])["total_profit"]
        .sum()
        .reset_index()
        .sort_values("total_profit", ascending=False)
    )

    fig_grouped = px.bar(
        person_cat_df,
        x="person",                  # ← Person on X axis
        y="total_profit",            # ← Profit on Y axis
        color="category",
        barmode="stack",             # ← Stacked! Much cleaner than grouped
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={"total_profit": "Total Profit ($)", "person": ""}
    )
    fig_grouped.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=450,
        legend_title="Category",
        xaxis_tickangle=-35,         # ← Angled labels
        margin=dict(l=20, r=20, t=20, b=120)
    )
    st.plotly_chart(fig_grouped, use_container_width=True)

# --- Chart 4: Profit Margin % by Person (Bar Chart)
with col_right2:
    st.subheader("Profit Margin % by Person")

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
    st.plotly_chart(fig_margin, use_container_width=True)
    
# -----------------------------------------------------------------------------
# 9. TABLE
# -----------------------------------------------------------------------------

st.markdown("---")
st.subheader("Full Breakdown")

display_df = filtered_df.copy()

# Clean up year/quarter display
display_df["order_year"]    = display_df["order_year"].astype(int)
display_df["order_quarter"] = display_df["order_quarter"].astype(int).map(quarter_labels)

# Rename columns for display
display_df.columns = [
    "Person", "Category", "Year", "Quarter", "Total Orders", "Total Quantity",
    "Total Sales", "Total Profit", "Total Shipping Cost",
    "Avg Discount %", "Profit Margin %"
]

# Numbers here stay numeric, Streamlit handles the formatting
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Total Sales": st.column_config.NumberColumn(
            "Total Sales",
            format="$ %,.2f",
        ),
        "Total Profit": st.column_config.NumberColumn(
            "Total Profit",
            format="$ %,.2f",
        ),
        "Total Shipping Cost": st.column_config.NumberColumn(
            "Total Shipping Cost",
            format="$ %,.2f",
        ),
        "Avg Discount %": st.column_config.NumberColumn(
            "Avg Discount %",
            format="%.1f%%",
        ),
        "Profit Margin %": st.column_config.NumberColumn(
            "Profit Margin %",
            format="%.2f%%",
        ),
        "Total Orders": st.column_config.NumberColumn(
            "Total Orders",
            format="%d",
        ),
        "Total Quantity": st.column_config.NumberColumn(
            "Total Quantity",
            format="%d",
        ),
    }
)