# Simple Analytics Dashboard

This repository contains a Python script (`demo.py`) that launches a simple analytics dashboard using the Streamlit library. The dashboard visualizes dummy business performance metrics.

## Features

*   **Dynamic Data Generation:** Generates random data for sales, revenue, customer segments, and transactions each time it runs or when refreshed.
*   **Key Metrics Display:** Shows summary cards for Total Sales, Average Monthly Revenue, and Total Customers.
*   **Visualizations:**
    *   Bar chart: Sales by Category
    *   Line chart: Monthly Revenue Trend
    *   Pie chart: Customer Segments
    *   Table: Recent Transactions
*   **Interactive Controls:**
    *   Refresh button to generate new dummy data.
    *   (Planned) Data filters for date ranges and categories.
    *   (Planned) Additional charts like scatter plots.
    *   (Planned) Enhanced interactivity like tooltips on charts.

## Purpose

This application serves as a demonstration of how to build a simple interactive dashboard with Python and Streamlit. It's a good starting point for anyone looking to visualize data quickly and effectively.

## How to Run

1.  **Ensure you have Python installed.**
2.  **Install Streamlit and other necessary libraries:**
    ```bash
    pip install streamlit pandas matplotlib numpy
    ```
3.  **Navigate to the directory containing `demo.py` in your terminal.**
4.  **Run the Streamlit application:**
    ```bash
    streamlit run demo.py
    ```
This will open the dashboard in your default web browser.

## Future Enhancements (In Progress)

This dashboard is currently being enhanced with the following features:
*   Data filters (date range, category selection).
*   Additional visualizations (e.g., scatter plot).
*   Improved interactive elements (tooltips, potentially clickable charts).
*   Enhanced layout and styling.
