import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
 
# Set page configuration
st.set_page_config(
    page_title="Simple Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)
 
# Add title and description
st.title("Simple Analytics Dashboard")
st.markdown("A visualization of business performance metrics using dummy data")
 
# Generate dummy data
def generate_dummy_data():
    # Sales by category
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home']
    sales = np.random.randint(1000, 5000, size=len(categories))
    sales_df = pd.DataFrame({'Category': categories, 'Sales': sales})
   
    # Monthly revenue (time series)
    today = datetime.now()
    dates = [(today - timedelta(days=30*i)).strftime('%Y-%m') for i in range(12)]
    dates.reverse()  # Start from the oldest
    revenue = np.cumsum(np.random.randint(500, 1500, size=len(dates)))
    revenue_df = pd.DataFrame({'Month': dates, 'Revenue': revenue})
   
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
 
# Display summary metrics in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Sales", value=f"${sales_df['Sales'].sum():,}")
with col2:
    st.metric(label="Avg Monthly Revenue", value=f"${int(revenue_df['Revenue'].mean()):,}")
with col3:
    st.metric(label="Total Customers", value=f"{customers_df['Customers'].sum():,}")
 
# Create two columns for charts
col1, col2 = st.columns(2)
 
# Bar chart in first column
with col1:
    st.subheader("Sales by Category")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(sales_df['Category'], sales_df['Sales'], color='skyblue')
    ax.set_ylabel('Sales ($)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)
 
# Line chart in second column
with col2:
    st.subheader("Monthly Revenue Trend")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(revenue_df['Month'], revenue_df['Revenue'], marker='o', linestyle='-', color='green')
    ax.set_ylabel('Revenue ($)')
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)
 
# Create two more columns for pie chart and table
col1, col2 = st.columns(2)
 
# Pie chart in first column
with col1:
    st.subheader("Customer Segments")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(customers_df['Customers'], labels=customers_df['Segment'], autopct='%1.1f%%',
           colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    st.pyplot(fig)
 
# Table in second column
with col2:
    st.subheader("Recent Transactions")
    st.dataframe(transactions_df)
 
# Footer
st.markdown("---")
st.markdown("Analytics Dashboard | Jules Enhancement Demo")