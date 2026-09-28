import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_data
from src.business_analysis import *
from src.visualization import *

st.set_page_config(page_title="Logistics Analytics Dashboard", layout="wide")


def normalize_dashboard_df(df):
    df = df.copy()
    for col in ['order_date', 'dispatch_date', 'expected_delivery_date', 'actual_delivery_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


@st.cache_data
def load_dashboard_data():
    return normalize_dashboard_df(load_data('data/cleaned/logistics_cleaned.csv'))


def show_sidebar_filters(df):
    st.sidebar.header("Filter Options")
    wh = st.sidebar.multiselect("Warehouse", options=df['warehouse'].unique())
    mode = st.sidebar.multiselect("Shipping Mode", options=df['shipping_mode'].unique())
    partner = st.sidebar.multiselect("Delivery Partner", options=df['delivery_partner'].unique())
    
    filtered_df = df.copy()
    if wh:
        filtered_df = filtered_df[filtered_df['warehouse'].isin(wh)]
    if mode:
        filtered_df = filtered_df[filtered_df['shipping_mode'].isin(mode)]
    if partner:
        filtered_df = filtered_df[filtered_df['delivery_partner'].isin(partner)]
    return filtered_df

def show_overview(df):
    st.title("Executive Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", calculate_total_orders(df))
    col2.metric("Delivered Orders", calculate_total_delivered(df))
    col3.metric("Delayed Orders", calculate_total_delayed(df))
    col4.metric("On-Time Rate", f"{calculate_on_time_percentage(df)}%")
    
    col5, col6 = st.columns(2)
    col5.metric("Total Logistics Cost", f"₹{calculate_total_logistics_cost(df):,.2f}")
    col6.metric("Avg Logistics Cost / Order", f"₹{calculate_average_logistics_cost(df):,.2f}")
    
    st.pyplot(plot_delivery_status(df))

def show_delivery_analysis(df):
    st.title("Delivery Performance Analysis")
    st.pyplot(plot_monthly_orders(df))
    st.pyplot(plot_monthly_delivery_performance(df))
    st.pyplot(plot_delay_distribution(df))

def show_route_analysis(df):
    st.title("Route & Logistics Analysis")
    st.pyplot(plot_delay_by_route(df))
    st.pyplot(plot_cost_by_route(df))

def show_warehouse_analysis(df):
    st.title("Warehouse Operational Analysis")
    st.pyplot(plot_orders_by_warehouse(df))
    st.pyplot(plot_processing_time_by_warehouse(df))
    st.pyplot(plot_delay_by_warehouse(df))

def show_cost_analysis(df):
    st.title("Cost Breakdown Analytics")
    st.pyplot(plot_cost_by_shipping_mode(df))
    st.pyplot(plot_cost_trend(df))

def show_partner_analysis(df):
    st.title("Delivery Partner Benchmarking")
    st.pyplot(plot_shipments_by_partner(df))
    st.pyplot(plot_partner_delivery_performance(df))
    st.pyplot(plot_partner_cost(df))

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Executive Overview", 
        "Delivery Analysis", 
        "Route Analysis", 
        "Warehouse Analysis", 
        "Cost Analysis", 
        "Partner Analysis"
    ])

    raw_df = normalize_dashboard_df(load_dashboard_data())
    df = show_sidebar_filters(raw_df)
    
    if page == "Executive Overview":
        show_overview(df)
    elif page == "Delivery Analysis":
        show_delivery_analysis(df)
    elif page == "Route Analysis":
        show_route_analysis(df)
    elif page == "Warehouse Analysis":
        show_warehouse_analysis(df)
    elif page == "Cost Analysis":
        show_cost_analysis(df)
    elif page == "Partner Analysis":
        show_partner_analysis(df)

if __name__ == "__main__":
    main()