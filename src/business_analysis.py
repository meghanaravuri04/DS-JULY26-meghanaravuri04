import pandas as pd

def calculate_total_orders(df: pd.DataFrame) -> int:
    """Return the total count of unique orders."""
    return int(df['order_id'].nunique())

def calculate_total_delivered(df: pd.DataFrame) -> int:
    """Return count of successfully delivered orders."""
    return int((df['delivery_status'] == 'Delivered').sum())

def calculate_total_delayed(df: pd.DataFrame) -> int:
    """Return count of delayed orders."""
    return int((df['delivery_status'] == 'Delayed').sum())

def calculate_on_time_percentage(df: pd.DataFrame) -> float:
    """Calculate the percentage of orders delivered on time."""
    return round(float(df['on_time_flag'].mean() * 100), 2)

def calculate_average_delivery_days(df: pd.DataFrame) -> float:
    """Calculate average delivery days from dispatch to actual delivery."""
    return round(float(df['delivery_days'].mean()), 2)

def calculate_average_delay_days(df: pd.DataFrame) -> float:
    """Calculate average delay in days for delayed shipments."""
    delayed = df[df['delay_days'] > 0]
    return round(float(delayed['delay_days'].mean()), 2) if len(delayed) > 0 else 0.0

def calculate_total_shipping_cost(df: pd.DataFrame) -> float:
    """Calculate total shipping cost across all orders."""
    return round(float(df['shipping_cost'].sum()), 2)

def calculate_average_shipping_cost(df: pd.DataFrame) -> float:
    """Calculate average shipping cost per order."""
    return round(float(df['shipping_cost'].mean()), 2)

def calculate_total_fuel_cost(df: pd.DataFrame) -> float:
    """Calculate cumulative fuel cost."""
    return round(float(df['fuel_cost'].sum()), 2)

def calculate_total_logistics_cost(df: pd.DataFrame) -> float:
    """Calculate total logistics cost (shipping cost + fuel cost)."""
    return round(float(df['total_logistics_cost'].sum()), 2)

def calculate_average_logistics_cost(df: pd.DataFrame) -> float:
    """Calculate average total logistics cost per order."""
    return round(float(df['total_logistics_cost'].mean()), 2)

def calculate_average_cost_per_km(df: pd.DataFrame) -> float:
    """Calculate overall average cost per kilometer."""
    return round(float(df['cost_per_km'].mean()), 2)

def analyze_route_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Group metrics by route for volume, delay, and cost analysis."""
    return df.groupby('route').agg(
        order_count=('order_id', 'count'),
        avg_delay_days=('delay_days', 'mean'),
        avg_total_cost=('total_logistics_cost', 'mean'),
        avg_cost_per_km=('cost_per_km', 'mean')
    ).reset_index()

def analyze_route_cost(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze total and average cost by route."""
    return df.groupby('route')['total_logistics_cost'].agg(['sum', 'mean']).reset_index()

def analyze_route_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze delay metrics across transportation routes."""
    return df.groupby('route')['delay_days'].mean().reset_index()

def analyze_warehouse_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze warehouse processing, volumes, and delay rates."""
    return df.groupby('warehouse').agg(
        total_orders=('order_id', 'count'),
        avg_processing_hours=('warehouse_processing_hours', 'mean'),
        on_time_pct=('on_time_flag', lambda x: x.mean() * 100)
    ).reset_index()

def analyze_warehouse_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Compute delay percentage per warehouse."""
    return df.groupby('warehouse')['on_time_flag'].apply(lambda x: (1 - x.mean()) * 100).reset_index(name='delay_pct')

def analyze_warehouse_processing_time(df: pd.DataFrame) -> pd.DataFrame:
    """Compute average processing hours per warehouse."""
    return df.groupby('warehouse')['warehouse_processing_hours'].mean().reset_index()

def analyze_shipping_mode(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze shipment distribution across shipping modes."""
    return df['shipping_mode'].value_counts().reset_index()

def analyze_shipping_mode_cost(df: pd.DataFrame) -> pd.DataFrame:
    """Compare average cost across shipping modes."""
    return df.groupby('shipping_mode')['total_logistics_cost'].mean().reset_index()

def analyze_shipping_mode_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Compare delay rates across shipping modes."""
    return df.groupby('shipping_mode')['on_time_flag'].apply(lambda x: (1 - x.mean()) * 100).reset_index(name='delay_pct')

def analyze_delivery_partner(df: pd.DataFrame) -> pd.DataFrame:
    """Evaluate partner performance across volume, on-time percentage, and cost."""
    return df.groupby('delivery_partner').agg(
        total_shipments=('order_id', 'count'),
        on_time_pct=('on_time_flag', lambda x: x.mean() * 100),
        avg_cost=('shipping_cost', 'mean'),
        damage_rate=('damage_flag', lambda x: x.mean() * 100)
    ).reset_index()

def analyze_partner_cost(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze average shipping cost per delivery partner."""
    return df.groupby('delivery_partner')['shipping_cost'].mean().reset_index()

def analyze_partner_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze delay percentage per delivery partner."""
    return df.groupby('delivery_partner')['on_time_flag'].apply(lambda x: (1 - x.mean()) * 100).reset_index(name='delay_pct')

def analyze_partner_damage_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze shipment damage rate by delivery partner."""
    return df.groupby('delivery_partner')['damage_flag'].mean().apply(lambda x: x * 100).reset_index()

def calculate_average_customer_rating(df: pd.DataFrame) -> float:
    """Calculate overall average customer satisfaction score."""
    return round(float(df['customer_rating'].mean()), 2)

def calculate_return_rate(df: pd.DataFrame) -> float:
    """Calculate overall return rate percentage."""
    return round(float(df['return_flag'].mean() * 100), 2)

def calculate_damage_rate(df: pd.DataFrame) -> float:
    """Calculate overall shipment damage rate percentage."""
    return round(float(df['damage_flag'].mean() * 100), 2)