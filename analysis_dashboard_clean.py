import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - COMPACT / MODERN DASHBOARD
# ============================================================
st.markdown("""
<style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1500px;
    }

    .dashboard-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 0.05rem;
    }

    .dashboard-subtitle {
        font-size: 1rem;
        opacity: 0.75;
        margin-bottom: 1rem;
    }

    div[data-testid="stMetric"] {
        padding: 12px 14px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.22);
        min-height: 92px;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.45rem;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 0.4rem;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_customer_behavior_dataset_v2.csv")

    # Convert date column
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Dataset not found. Keep 'ecommerce_customer_behavior_dataset_v2.csv' "
        "in the same folder as analysis.py."
    )
    st.stop()
except Exception as e:
    st.error(f"Could not load the dataset: {e}")
    st.stop()


# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.title("🔎 Dashboard Filters")
st.sidebar.caption("Use the filters below to update the dashboard.")

filtered_df = df.copy()

# Date filter
if "Date" in df.columns and df["Date"].notna().any():
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    selected_dates = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered_df = filtered_df[
            (filtered_df["Date"].dt.date >= start_date) &
            (filtered_df["Date"].dt.date <= end_date)
        ]

# Generic categorical filters
filter_columns = [
    ("Gender", "👤 Gender"),
    ("City", "🏙️ City"),
    ("Product_Category", "📦 Product Category"),
    ("Payment_Method", "💳 Payment Method"),
    ("Device", "💻 Device"),
    ("Customer_Rating", "⭐ Customer Rating"),
    ("Returning_Customer", "🔁 Returning Customer")
]

for column, label in filter_columns:
    if column in df.columns:
        options = sorted(df[column].dropna().unique().tolist(), key=str)
        selected = st.sidebar.multiselect(
            label,
            options,
            default=options
        )

        if selected:
            filtered_df = filtered_df[
                filtered_df[column].isin(selected)
            ]

# Filter result
st.sidebar.divider()
st.sidebar.info(
    f"Showing {len(filtered_df):,} of {len(df):,} records "
    f"({(len(filtered_df) / len(df) * 100) if len(df) else 0:.1f}%)"
)


# ============================================================
# TITLE - VERY TOP
# ============================================================
st.markdown(
    '<div class="dashboard-title">📊 E-Commerce Sales Dashboard</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="dashboard-subtitle">Customer Behavior & Sales Analysis</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI CARDS
# ============================================================
if "Total_Amount" in filtered_df.columns:
    total_revenue = pd.to_numeric(
        filtered_df["Total_Amount"], errors="coerce"
    ).sum()
    average_order_value = pd.to_numeric(
        filtered_df["Total_Amount"], errors="coerce"
    ).mean()
else:
    total_revenue = 0
    average_order_value = 0

total_orders = (
    filtered_df["Order_ID"].nunique()
    if "Order_ID" in filtered_df.columns else len(filtered_df)
)

total_customers = (
    filtered_df["Customer_ID"].nunique()
    if "Customer_ID" in filtered_df.columns else 0
)

st.markdown('<div class="section-title">📌 Key Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")

with col2:
    st.metric("🛒 Total Orders", f"{total_orders:,}")

with col3:
    st.metric("👥 Total Customers", f"{total_customers:,}")

with col4:
    st.metric("📦 Average Order Value", f"₹{average_order_value:,.2f}")


st.divider()


# ============================================================
# EMPTY FILTER RESULT CHECK
# ============================================================
if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()


# ============================================================
# CHART 1 + CHART 2
# ============================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Sales by Product Category")

    if {"Product_Category", "Total_Amount"}.issubset(filtered_df.columns):
        category_sales = (
            filtered_df.groupby("Product_Category")["Total_Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        fig_category = px.bar(
            x=category_sales.index,
            y=category_sales.values,
            labels={
                "x": "Product Category",
                "y": "Total Sales (₹)"
            },
            title="Revenue by Product Category"
        )

        fig_category.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=55, b=20),
            showlegend=False
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with col2:
    st.subheader("📈 Monthly Sales Trend")

    if {"Date", "Total_Amount"}.issubset(filtered_df.columns):
        monthly_sales = (
            filtered_df.dropna(subset=["Date"])
            .assign(Month=lambda x: x["Date"].dt.to_period("M").astype(str))
            .groupby("Month")["Total_Amount"]
            .sum()
            .reset_index()
        )

        fig_monthly = px.line(
            monthly_sales,
            x="Month",
            y="Total_Amount",
            markers=True,
            labels={
                "Month": "Month",
                "Total_Amount": "Revenue (₹)"
            },
            title="Monthly Revenue Trend"
        )

        fig_monthly.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=55, b=20)
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True,
            config={"displayModeBar": False}
        )


# ============================================================
# CHART 3 + CHART 4
# ============================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏙️ Top Cities by Revenue")

    if {"City", "Total_Amount"}.issubset(filtered_df.columns):
        city_sales = (
            filtered_df.groupby("City")["Total_Amount"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .sort_values(ascending=True)
        )

        fig_city = px.bar(
            x=city_sales.values,
            y=city_sales.index,
            orientation="h",
            labels={
                "x": "Revenue (₹)",
                "y": "City"
            },
            title="Top 10 Cities by Revenue"
        )

        fig_city.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=55, b=20),
            showlegend=False
        )

        st.plotly_chart(
            fig_city,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with col2:
    st.subheader("💳 Sales by Payment Method")

    if {"Payment_Method", "Total_Amount"}.issubset(filtered_df.columns):
        payment_sales = (
            filtered_df.groupby("Payment_Method")["Total_Amount"]
            .sum()
            .sort_values(ascending=False)
        )

        fig_payment = px.bar(
            x=payment_sales.index,
            y=payment_sales.values,
            labels={
                "x": "Payment Method",
                "y": "Revenue (₹)"
            },
            title="Revenue by Payment Method"
        )

        fig_payment.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=55, b=20),
            showlegend=False
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True,
            config={"displayModeBar": False}
        )


# ============================================================
# CHART 5 + CHART 6
# ============================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("💻 Customer Device Distribution")

    if "Device" in filtered_df.columns:
        device_counts = filtered_df["Device"].value_counts()

        fig_device = px.pie(
            values=device_counts.values,
            names=device_counts.index,
            hole=0.45,
            title="Customer Device Distribution"
        )

        fig_device.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=55, b=20)
        )

        st.plotly_chart(
            fig_device,
            use_container_width=True,
            config={"displayModeBar": False}
        )

with col2:
    st.subheader("⭐ Sales by Customer Rating")

    if {"Customer_Rating", "Total_Amount"}.issubset(filtered_df.columns):
        rating_sales = (
            filtered_df.groupby("Customer_Rating")["Total_Amount"]
            .sum()
            .sort_index()
        )

        fig_rating = px.bar(
            x=rating_sales.index,
            y=rating_sales.values,
            labels={
                "x": "Customer Rating",
                "y": "Total Sales (₹)"
            },
            title="Sales by Customer Rating"
        )

        fig_rating.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=55, b=20),
            showlegend=False
        )

        st.plotly_chart(
            fig_rating,
            use_container_width=True,
            config={"displayModeBar": False}
        )


# ============================================================
# FILTERED DATASET
# ============================================================
st.divider()
st.subheader("📋 Filtered Dataset")
st.caption(f"Displaying {len(filtered_df):,} filtered records")

st.dataframe(
    filtered_df,
    width="stretch",
    height=300
)
