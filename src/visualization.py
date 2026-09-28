import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid")


def _ensure_datetime_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Convert a date-like column to pandas datetime before resampling."""
    df = df.copy()
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')
    return df


def plot_delivery_status(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x='delivery_status', ax=ax, palette='Set2')
    ax.set_title('Delivery Status Distribution')
    ax.set_xlabel('Status')
    ax.set_ylabel('Order Count')
    plt.tight_layout()
    return fig

def plot_monthly_orders(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    df = _ensure_datetime_column(df, 'order_date')
    monthly = df.set_index('order_date').resample('ME')['order_id'].count().reset_index()
    sns.lineplot(data=monthly, x='order_date', y='order_id', marker='o', ax=ax, color='navy')
    ax.set_title('Monthly Order Trend')
    ax.set_xlabel('Month')
    ax.set_ylabel('Orders')
    plt.tight_layout()
    return fig

def plot_monthly_delivery_performance(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    df = _ensure_datetime_column(df, 'actual_delivery_date')
    monthly = df.set_index('actual_delivery_date').resample('ME')['on_time_flag'].mean().reset_index()
    monthly['on_time_pct'] = monthly['on_time_flag'] * 100
    sns.lineplot(data=monthly, x='actual_delivery_date', y='on_time_pct', marker='s', ax=ax, color='green')
    ax.set_title('Monthly On-Time Delivery Performance (%)')
    ax.set_xlabel('Month')
    ax.set_ylabel('On-Time %')
    plt.tight_layout()
    return fig

def plot_delay_by_warehouse(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    data = df.groupby('warehouse')['on_time_flag'].apply(lambda x: (1 - x.mean()) * 100).reset_index()
    sns.barplot(data=data, x='warehouse', y='on_time_flag', ax=ax, palette='Reds_r')
    ax.set_title('Delay Percentage by Warehouse')
    ax.set_ylabel('Delay Rate (%)')
    plt.tight_layout()
    return fig

def plot_delay_by_shipping_mode(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    data = df.groupby('shipping_mode')['on_time_flag'].apply(lambda x: (1 - x.mean()) * 100).reset_index()
    sns.barplot(data=data, x='shipping_mode', y='on_time_flag', ax=ax, palette='Oranges_r')
    ax.set_title('Delay Percentage by Shipping Mode')
    ax.set_ylabel('Delay Rate (%)')
    plt.tight_layout()
    return fig

def plot_delay_by_route(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    top_routes = df.groupby('route')['delay_days'].mean().nlargest(10).reset_index()
    sns.barplot(data=top_routes, y='route', x='delay_days', ax=ax, palette='Reds_r')
    ax.set_title('Top 10 Routes by Average Delay (Days)')
    ax.set_xlabel('Average Delay (Days)')
    plt.tight_layout()
    return fig

def plot_delay_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df[df['delay_days'] > 0]['delay_days'], bins=15, kde=True, ax=ax, color='coral')
    ax.set_title('Delay Days Distribution (Delayed Orders)')
    ax.set_xlabel('Delay (Days)')
    plt.tight_layout()
    return fig

def plot_cost_by_shipping_mode(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=df, x='shipping_mode', y='total_logistics_cost', ax=ax, palette='Blues_d')
    ax.set_title('Average Total Logistics Cost by Shipping Mode')
    ax.set_ylabel('Avg Cost (INR)')
    plt.tight_layout()
    return fig

def plot_cost_by_route(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    top_cost_routes = df.groupby('route')['total_logistics_cost'].mean().nlargest(10).reset_index()
    sns.barplot(data=top_cost_routes, y='route', x='total_logistics_cost', ax=ax, palette='Blues_r')
    ax.set_title('Top 10 Expensive Routes by Avg Cost')
    ax.set_xlabel('Avg Total Cost (INR)')
    plt.tight_layout()
    return fig

def plot_cost_trend(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    df = _ensure_datetime_column(df, 'order_date')
    monthly = df.set_index('order_date').resample('ME')['total_logistics_cost'].sum().reset_index()
    sns.lineplot(data=monthly, x='order_date', y='total_logistics_cost', marker='o', ax=ax, color='teal')
    ax.set_title('Monthly Total Logistics Expenditure')
    ax.set_ylabel('Total Cost (INR)')
    plt.tight_layout()
    return fig

def plot_orders_by_warehouse(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.countplot(data=df, x='warehouse', ax=ax, palette='Purples_r')
    ax.set_title('Order Volume by Warehouse')
    ax.set_ylabel('Order Count')
    plt.tight_layout()
    return fig

def plot_processing_time_by_warehouse(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=df, x='warehouse', y='warehouse_processing_hours', ax=ax, )
    ax.set_title('Average Processing Hours by Warehouse')
    ax.set_ylabel('Processing Time (Hours)')
    plt.tight_layout()
    return fig

def plot_shipments_by_partner(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(data=df, x='delivery_partner', ax=ax, palette='magma')
    ax.set_title('Shipment Count by Delivery Partner')
    ax.set_ylabel('Shipments')
    plt.tight_layout()
    return fig

def plot_partner_delivery_performance(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    data = df.groupby('delivery_partner')['on_time_flag'].mean().apply(lambda x: x * 100).reset_index()
    sns.barplot(data=data, x='delivery_partner', y='on_time_flag', ax=ax, palette='crest')
    ax.set_title('On-Time Delivery Rate (%) by Partner')
    ax.set_ylabel('On-Time Rate (%)')
    plt.tight_layout()
    return fig

def plot_partner_cost(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=df, x='delivery_partner', y='shipping_cost', ax=ax, palette='rocket')
    ax.set_title('Average Shipping Cost by Delivery Partner')
    ax.set_ylabel('Avg Shipping Cost (INR)')
    plt.tight_layout()
    return fig

def plot_customer_rating_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(df['customer_rating'], discrete=True, ax=ax, color='goldenrod')
    ax.set_title('Customer Rating Distribution')
    ax.set_xlabel('Rating (1-5)')
    plt.tight_layout()
    return fig

def plot_rating_by_delivery_status(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x='delivery_status', y='customer_rating', ax=ax, palette='Set3')
    ax.set_title('Customer Rating by Delivery Status')
    ax.set_ylabel('Rating')
    plt.tight_layout()
    return fig