# Logistics Delivery Performance & Cost Analytics

A comprehensive data analytics and business intelligence solution designed to analyze logistics operational performance, identify bottlenecks, evaluate carrier performance, and monitor delivery costs across regional supply chains.

---

## Executive Summary

Management across logistics operations faces challenges in identifying key drivers behind delivery delays, warehouse processing inefficiencies, and high transport expenditure. This project delivers a standardized, modular Python pipeline to process raw shipment data, perform end-to-end data cleaning, execute exploratory data analysis (EDA), compute operational KPIs, and surface real-time actionable insights through an interactive Streamlit dashboard.

---

## Business Objectives & Key Questions Answered

### 1. Delivery Performance
* **Total Volume & On-Time Rate:** How many orders are delivered on time vs. delayed?
* **SLA Metrics:** What are the average delivery times and delay durations across orders?

### 2. Route & Transit Efficiency
* **Congestion & Delays:** Which routes suffer from the longest operational delays?
* **Cost Allocation:** Which transit corridors exhibit the highest total cost and cost-per-kilometer?

### 3. Warehouse Operations
* **Processing Lead Times:** Which warehouses take the longest to process shipments?
* **Bottleneck Identification:** Which handling centers account for the highest delay percentages?

### 4. Shipping Mode & Carrier Benchmarking
* **Mode Analysis:** How do Road, Rail, Air, and Express shipping modes compare in cost and delay rates?
* **Partner Performance:** Which delivery partners achieve the highest on-time delivery rates and lowest package damage rates?

---

## Technology Stack

* **Programming Language:** Python 3.10+
* **Data Processing & Analytics:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn
* **Interactive Dashboard:** Streamlit[cite: 1]
* **Testing:** pytest[cite: 1]
* **Development Environment:** Jupyter Notebook, VS Code / PyCharm[cite: 1]

---

## Project Directory Structure

The repository follows a standardized modular structure[cite: 1]:

```text
logistics_delivery_analytics/
├── data/
│   ├── raw/
│   │   └── logistics_data.csv          # Original raw operational dataset
│   └── cleaned/
│       └── logistics_cleaned.csv       # Cleaned, standardized, and feature-engineered dataset
├── notebooks/
│   └── logistics_analysis.ipynb        # Complete exploratory analysis notebook
├── src/
│   ├── __init__.py
│   ├── data_loader.py                  # Module for loading raw data safely
│   ├── data_cleaner.py                 # Pipeline functions for data cleaning & feature creation
│   ├── business_analysis.py            # Core business analytics & KPI functions
│   └── visualization.py                # Reusable plotting & visualization functions
├── app/
│   └── streamlit_app.py                # Multi-page interactive Streamlit dashboard
├── reports/
│   └── business_report.md              # Comprehensive executive report
├── tests/
│   └── test_pipeline.py                # Unit tests for the data cleaning pipeline and KPIs
├── .gitignore                          # Excluded files and folders
├── requirements.txt                    # Project dependencies
├── README.md                           # Project documentation
└── run_pipeline.py                     # Execution script for the data pipeline