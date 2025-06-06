import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import random # Added random import
 
# Set page configuration
st.set_page_config(
    page_title="Simple Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)
 
# Add title and description
st.title("Simple Analytics Dashboard")
st.markdown("A visualization of business performance metrics using dummy data")
st.markdown("Use the filters in the sidebar to explore different segments of the data.")

# Sidebar placeholder
st.sidebar.title("Filters")
# st.sidebar.markdown("Filter controls will be here.") # Removed placeholder
 
# Generate dummy data
def generate_dummy_data():
    today = datetime.now() # Moved today here for use in sales_df
    # Sales by category
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home']
    sales = np.random.randint(1000, 5000, size=len(categories))
    # Add 'Date' and 'Number of Customers'
    dates = [today - timedelta(days=random.randint(0, 364)) for _ in categories]
    num_customers = [random.randint(50, 200) for _ in categories]
    sales_df = pd.DataFrame({
        'Category': categories,
        'Sales': sales,
        'Date': dates,
        'Number of Customers': num_customers
    })
   
    # Monthly revenue (time series)
    # today = datetime.now() # No longer needed here
    month_dates = [(today - timedelta(days=30*i)).strftime('%Y-%m') for i in range(12)]
    month_dates.reverse()  # Start from the oldest
    revenue = np.cumsum(np.random.randint(500, 1500, size=len(month_dates)))
    revenue_df = pd.DataFrame({'Month': month_dates, 'Revenue': revenue})
   
    # Customer segments
    segments = ['New', 'Returning', 'VIP', 'Inactive']
    customers = np.random.randint(100, 500, size=len(segments))
    customers_df = pd.DataFrame({'Segment': segments, 'Customers': customers})
   
    # Recent transactions
    products = ['Laptop', 'T-shirt', 'Groceries', 'Novel', 'Chair', 'Phone', 'Headphones', 'Shoes']
    transactions = []
    for i in range(10):
        transactions.append({
            'ID': f'TRX-{1000+i}',
            'Date': (today - timedelta(days=i)).strftime('%Y-%m-%d'),
            'Product': np.random.choice(products),
            'Amount': np.random.randint(10, 500)
        })
    transactions_df = pd.DataFrame(transactions)
   
    return sales_df, revenue_df, customers_df, transactions_df
 
# Create refresh button
if st.button('Refresh Data'):
    st.success('Data refreshed successfully!')
 
# Generate data
sales_df, revenue_df, customers_df, transactions_df = generate_dummy_data()

# Convert date/month columns to datetime objects for filtering
revenue_df['Month_dt'] = pd.to_datetime(revenue_df['Month'] + '-01')
transactions_df['Date_dt'] = pd.to_datetime(transactions_df['Date'])

# --- Sidebar Filters ---
st.sidebar.header("Date Range Filter")

# Determine overall min and max dates for date inputs
min_revenue_date = revenue_df['Month_dt'].min().date()
max_revenue_date = revenue_df['Month_dt'].max().date()
min_transaction_date = transactions_df['Date_dt'].min().date()
max_transaction_date = transactions_df['Date_dt'].max().date()

overall_min_date = min(min_revenue_date, min_transaction_date)
overall_max_date = max(max_revenue_date, max_transaction_date)

start_date = st.sidebar.date_input("Start date", overall_min_date,
                                   min_value=overall_min_date, max_value=overall_max_date)
end_date = st.sidebar.date_input("End date", overall_max_date,
                                 min_value=overall_min_date, max_value=overall_max_date)

st.sidebar.header("Category Filter")
all_categories = sales_df['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories",
                                             options=all_categories,
                                             default=all_categories)

# --- Filter DataFrames based on sidebar inputs ---
# Convert sidebar date inputs to datetime objects for comparison
start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

# Filter sales_df by category
if selected_categories:
    filtered_sales_df = sales_df[sales_df['Category'].isin(selected_categories)]
else:
    filtered_sales_df = sales_df.copy() # Use all categories if none are selected

# Filter revenue_df by date range
filtered_revenue_df = revenue_df[
    (revenue_df['Month_dt'] >= start_datetime) & (revenue_df['Month_dt'] <= end_datetime)
]

# Filter transactions_df by date range
filtered_transactions_df = transactions_df[
    (transactions_df['Date_dt'] >= start_datetime) & (transactions_df['Date_dt'] <= end_datetime)
]

# --- Main Page Layout ---

# Display summary metrics in columns (using original full data for these for now)
# Or, these could also be updated based on filters if desired.
# For this task, instructions focused on charts and tables.
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Sales", value=f"${sales_df['Sales'].sum():,}") # Original total sales
with col2:
    # Avg Monthly Revenue could be from filtered_revenue_df if desired
    avg_rev = filtered_revenue_df['Revenue'].mean() if not filtered_revenue_df.empty else 0
    st.metric(label="Avg Monthly Revenue (filtered)", value=f"${int(avg_rev):,}")
with col3:
    st.metric(label="Total Customers", value=f"{customers_df['Customers'].sum():,}") # Original customer data

# Create two columns for charts
col1, col2 = st.columns(2)
 
# Bar chart in first column (using filtered_sales_df)
with col1:
    st.subheader("Sales by Category")
    if not filtered_sales_df.empty:
        st.bar_chart(filtered_sales_df.set_index('Category')['Sales'])
    else:
        st.warning("No data to display for selected categories.")

# Line chart in second column (using filtered_revenue_df)
with col2:
    st.subheader("Monthly Revenue Trend")
    if not filtered_revenue_df.empty:
        # Using Month_dt for proper time series indexing
        st.line_chart(filtered_revenue_df.set_index('Month_dt')['Revenue'])
    else:
        # The previous check for matplotlib is now handled by this
        st.warning("No revenue data to display for selected date range.")
 
# Create two more columns for pie chart and table
col3, col4 = st.columns(2) # Changed to col3, col4 to avoid conflict with col1, col2 above
 
# Pie chart in first column (customer segments not filtered by date/category in this version)
with col3: # Changed to col3
    st.subheader("Customer Segments")
    fig, ax = plt.subplots(figsize=(8, 8)) # Matplotlib pie chart remains
    ax.pie(customers_df['Customers'], labels=customers_df['Segment'], autopct='%1.1f%%',
           colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    st.pyplot(fig)
 
# Table in second column (using filtered_transactions_df)
with col4: # Changed to col4
    st.subheader("Recent Transactions")
    if not filtered_transactions_df.empty:
        st.dataframe(filtered_transactions_df[['ID', 'Date', 'Product', 'Amount']]) # Display original Date string
    else:
        st.warning("No transactions to display for selected date range.")

# New Row for Scatter Plot
st.subheader("Sales vs. Customers by Category")
if not filtered_sales_df.empty:
    st.scatter_chart(filtered_sales_df, x='Number of Customers', y='Sales', color='Category')
else:
    st.warning("No sales data to display for scatter plot based on selected categories.")

# Footer
st.markdown("---")
st.markdown("Analytics Dashboard | Jules Enhancement Demo")