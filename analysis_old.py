import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
df = pd.read_csv("ecommerce_customer_behavior_dataset_v2.csv")

# Display basic information
print("Dataset loaded successfully!")
print("Rows and columns:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nData types:")
print(df.dtypes)
# ==============================
# BUSINESS ANALYSIS
# ==============================

print("\n========== BUSINESS ANALYSIS ==========")

# 1. Total Revenue
total_revenue = df["Total_Amount"].sum()
print("Total Revenue:", total_revenue)

# 2. Total Orders
total_orders = df["Order_ID"].nunique()
print("Total Orders:", total_orders)

# 3. Total Customers
total_customers = df["Customer_ID"].nunique()
print("Total Customers:", total_customers)

# 4. Average Order Value
average_order_value = df["Total_Amount"].mean()
print("Average Order Value:", average_order_value)

# 5. Top Product Categories
print("\nTop Product Categories:")
print(df["Product_Category"].value_counts().head(10))

# 6. Sales by City
print("\nTop Cities by Orders:")
print(df["City"].value_counts().head(10))

# 7. Payment Methods
print("\nPayment Methods:")
print(df["Payment_Method"].value_counts())

# 8. Device Types
print("\nDevice Types:")
print(df["Device_Type"].value_counts())

# 9. Returning vs New Customers
print("\nReturning Customer Status:")
print(df["Is_Returning_Customer"].value_counts())

# 10. Average Customer Rating
average_rating = df["Customer_Rating"].mean()
print("\nAverage Customer Rating:", average_rating)

import matplotlib.pyplot as plt

# 11. Sales by Product Category
category_sales = df.groupby("Product_Category")["Total_Amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
category_sales.plot(kind="bar")

plt.title("Sales by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

# 12. Monthly Sales Trend

df["Date"] = pd.to_datetime(df["Date"])

monthly_sales = (
    df.groupby(df["Date"].dt.to_period("M"))["Total_Amount"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

# 13. Sales by City
city_sales = df.groupby("City")["Total_Amount"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
city_sales.plot(kind="bar")

plt.title("Top 10 Cities by Sales")
plt.xlabel("City")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

# 14. Sales by Payment Method
payment_sales = df.groupby("Payment_Method")["Total_Amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
payment_sales.plot(kind="bar")

plt.title("Sales by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

# 15. Sales by Device Type
device_sales = df.groupby("Device_Type")["Total_Amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
device_sales.plot(kind="bar")

plt.title("Sales by Device Type")
plt.xlabel("Device Type")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

# 16. Sales by Returning Customer Status
returning_sales = df.groupby("Is_Returning_Customer")["Total_Amount"].sum()

plt.figure(figsize=(8, 5))
returning_sales.plot(kind="bar")

plt.title("Sales by Returning Customer Status")
plt.xlabel("Returning Customer")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

# 17. Sales by Customer Rating
rating_sales = df.groupby("Customer_Rating")["Total_Amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
rating_sales.plot(kind="bar")

plt.title("Sales by Customer Rating")
plt.xlabel("Customer Rating")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

# 18. Sales by Gender
gender_sales = df.groupby("Gender")["Total_Amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
gender_sales.plot(kind="bar")

plt.title("Sales by Gender")
plt.xlabel("Gender")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

# 19. Sales by Age Group

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 18, 25, 35, 45, 55, 100],
    labels=["Under 18", "18-25", "26-35", "36-45", "46-55", "56+"]
)

age_group_sales = (
    df.groupby("Age_Group", observed=True)["Total_Amount"]
    .sum()
)

plt.figure(figsize=(10, 6))
age_group_sales.plot(kind="bar")

plt.title("Sales by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

# 20. Key Business Metrics Summary

print("\n" + "=" * 45)
print("       KEY BUSINESS METRICS SUMMARY")
print("=" * 45)

print(f"Total Revenue: ₹{df['Total_Amount'].sum():,.2f}")
print(f"Total Orders: {df['Order_ID'].nunique():,}")
print(f"Total Customers: {df['Customer_ID'].nunique():,}")
print(f"Average Order Value: ₹{df['Total_Amount'].mean():,.2f}")
print(f"Average Customer Rating: {df['Customer_Rating'].mean():.2f}")

print("=" * 45)

# 21. Sales by Customer Rating

rating_sales = df.groupby("Customer_Rating")["Total_Amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
rating_sales.plot(kind="bar")

plt.title("Sales by Customer Rating")
plt.xlabel("Customer Rating")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()

st.pyplot(plt.gcf())
plt.close()

import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_customer_behavior_dataset_v2.csv")
    
    # Convert date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    
    return df

df = load_data()

# ==========================================
# INTERACTIVE FILTERS
# ==========================================

st.sidebar.header("🔎 Dashboard Filters")

# Date Filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "📅 Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# City Filter
cities = sorted(df["City"].dropna().unique())

selected_cities = st.sidebar.multiselect(
    "🌍 Select City",
    cities,
    default=cities
)

# Gender Filter
genders = sorted(df["Gender"].dropna().unique())

selected_genders = st.sidebar.multiselect(
    "👤 Gender",
    genders,
    default=genders
)

# Product Category
categories = sorted(df["Product_Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "📦 Product Category",
    categories,
    default=categories
)

# Payment Method
payment_methods = sorted(df["Payment_Method"].dropna().unique())

selected_payment = st.sidebar.multiselect(
    "💳 Payment Method",
    payment_methods,
    default=payment_methods
)

# Device Type
devices = sorted(df["Device_Type"].dropna().unique())

selected_devices = st.sidebar.multiselect(
    "📱 Device Type",
    devices,
    default=devices
)

# Customer Rating
ratings = sorted(df["Customer_Rating"].dropna().unique())

selected_ratings = st.sidebar.multiselect(
    "⭐ Customer Rating",
   ratings,
    default=ratings
)


# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df.copy()

# Date filter
if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date) &
        (filtered_df["Date"].dt.date <= end_date)
    ]

# City
filtered_df = filtered_df[
    filtered_df["City"].isin(selected_cities)
]

# Gender
filtered_df = filtered_df[
    filtered_df["Gender"].isin(selected_genders)
]

# Product Category
filtered_df = filtered_df[
    filtered_df["Product_Category"].isin(selected_categories)
]

# Payment Method
filtered_df = filtered_df[
    filtered_df["Payment_Method"].isin(selected_payment)
]

# Device Type
filtered_df = filtered_df[
    filtered_df["Device_Type"].isin(selected_devices)
]

# Customer Rating
filtered_df = filtered_df[
    filtered_df["Customer_Rating"].isin(selected_ratings)
]

# Filter Result Indicator
st.info(
    f"🔎 Showing {len(filtered_df):,} records out of {len(df):,} total records "
    f"({len(filtered_df) / len(df) * 100:.1f}% of dataset)"
)

# ============================================================
# DASHBOARD CONTENT
# ============================================================

st.subheader("📊 Dashboard Overview")

# Filter Result Indicator
st.info(
    f"🔎 Showing *{len(filtered_df):,}* records out of "
    f"*{len(df):,}* total records "
    f"({(len(filtered_df) / len(df) * 100):.1f}% of dataset)"
)

# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Revenue",
    f"₹{total_revenue:,.2f}"
)

col2.metric(
    "🛒 Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "👥 Total Customers",
    f"{total_customers:,}"
)

col4.metric(
    "📦 Average Order Value",
    f"₹{average_order_value:,.2f}"
)

st.divider()

# ============================================================
# CHART 1 & CHART 2
# ============================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🛍️ Sales by Product Category")

    category_sales = (
        filtered_df.groupby("Product_Category")["Total_Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x=category_sales.index,
        y=category_sales.values,
        labels={
            "x": "Product Category",
            "y": "Total Sales (₹)"
        },
        title="Revenue by Product Category"
    )

    fig_category.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


with col2:
    st.subheader("📈 Monthly Sales Trend")

    monthly_sales = (
        filtered_df
        .groupby(filtered_df["Date"].dt.to_period("M"))["Total_Amount"]
        .sum()
        .reset_index()
    )

    monthly_sales["Date"] = monthly_sales["Date"].astype(str)

    fig_monthly = px.line(
        monthly_sales,
        x="Date",
        y="Total_Amount",
        markers=True,
        labels={
            "Date": "Month",
            "Total_Amount": "Revenue (₹)"
        },
        title="Monthly Revenue Trend"
    )

    fig_monthly.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

# ============================================================
# CHART 3 & CHART 4
# ============================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Customer Rating")

    rating_data = (
        filtered_df["Customer_Rating"]
        .value_counts()
        .sort_index()
    )

    fig_rating = px.bar(
        x=rating_data.index,
        y=rating_data.values,
        labels={
            "x": "Customer Rating",
            "y": "Number of Customers"
        },
        title="Customer Rating Distribution"
    )

    fig_rating.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )


with col2:
    st.subheader("💳 Payment Method")

    payment_data = (
        filtered_df["Payment_Method"]
        .value_counts()
        .reset_index()
    )

    payment_data.columns = ["Payment_Method", "Count"]

    fig_payment = px.pie(
        payment_data,
        names="Payment_Method",
        values="Count",
        hole=0.4,
        title="Payment Method Distribution"
    )

    fig_payment.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )

# ============================================================
# CHART 5 & CHART 6
# ============================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏙️ Sales by City")

    city_sales = (
        filtered_df.groupby("City")["Total_Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig_city = px.bar(
        city_sales,
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
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_city,
        use_container_width=True
    )


with col2:
    st.subheader("📱 Device Type")

    device_data = (
        filtered_df["Device_Type"]
        .value_counts()
        .reset_index()
    )

    device_data.columns = ["Device_Type", "Count"]

    fig_device = px.pie(
        device_data,
        names="Device_Type",
        values="Count",
        hole=0.4,
        title="Customer Device Distribution"
    )

    fig_device.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig_device,
        use_container_width=True
    )

# ============================================================
# FILTERED DATASET
# ============================================================

st.divider()

st.subheader("📋 Filtered Dataset")

st.caption(
    f"Displaying {len(filtered_df):,} filtered records"
)

st.dataframe(
    filtered_df,
    width="stretch",
    height=400
)