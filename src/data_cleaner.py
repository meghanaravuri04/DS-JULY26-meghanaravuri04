import pandas as pd
import numpy as np

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values using median for numeric and mode for categorical columns."""
    df = df.copy()
    numeric_cols = ['distance_km', 'quantity', 'weight_kg', 'shipping_cost', 
                    'fuel_cost', 'warehouse_processing_hours', 'customer_rating']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
            
    categorical_cols = ['warehouse', 'origin_city', 'destination_city', 
                        'product_category', 'shipping_mode', 'delivery_partner', 
                        'delivery_status', 'damage_flag', 'return_flag']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate order records from the DataFrame."""
    return df.drop_duplicates()

def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim whitespace and standardize string column capitalization."""
    df = df.copy()
    id_cols = ['order_id', 'customer_id']
    for col in id_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
            
    cat_cols = ['warehouse', 'origin_city', 'destination_city', 
                'product_category', 'shipping_mode', 'delivery_partner', 
                'delivery_status']
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    return df

def clean_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date columns to standard datetime objects."""
    df = df.copy()
    date_cols = ['order_date', 'dispatch_date', 'expected_delivery_date', 'actual_delivery_date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def validate_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Apply non-negative constraints and range validations to numeric columns."""
    df = df.copy()
    df['distance_km'] = df['distance_km'].apply(lambda x: max(0.0, float(x)))
    df['quantity'] = df['quantity'].apply(lambda x: max(1, int(x)))
    df['weight_kg'] = df['weight_kg'].apply(lambda x: max(0.0, float(x)))
    df['shipping_cost'] = df['shipping_cost'].apply(lambda x: max(0.0, float(x)))
    df['fuel_cost'] = df['fuel_cost'].apply(lambda x: max(0.0, float(x)))
    df['warehouse_processing_hours'] = df['warehouse_processing_hours'].apply(lambda x: max(0.0, float(x)))
    df['customer_rating'] = df['customer_rating'].clip(1.0, 5.0)
    return df

def validate_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Enforce business rules such as converting flag columns to binary indicators."""
    df = df.copy()
    for flag_col in ['damage_flag', 'return_flag']:
        if flag_col in df.columns:
            df[flag_col] = df[flag_col].astype(str).str.upper().apply(
                lambda x: 1 if x in ['YES', '1', 'TRUE', '1.0'] else 0
            )
    return df

def create_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Compute derived operational metrics and total cost figures."""
    df = df.copy()

    for col in ['dispatch_date', 'expected_delivery_date', 'actual_delivery_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    df['delivery_days'] = (df['actual_delivery_date'] - df['dispatch_date']).dt.days
    df['delay_days'] = (df['actual_delivery_date'] - df['expected_delivery_date']).dt.days
    df['cost_per_km'] = df.apply(
        lambda r: r['shipping_cost'] / r['distance_km'] if r['distance_km'] > 0 else 0.0, axis=1
    )
    df['total_logistics_cost'] = df['shipping_cost'] + df['fuel_cost']
    df['on_time_flag'] = df['delay_days'].apply(lambda x: 1 if pd.notna(x) and x <= 0 else 0)
    df['route'] = df['origin_city'].fillna('Unknown') + " -> " + df['destination_city'].fillna('Unknown')
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Master cleaning wrapper running all sequential data cleaning transformations."""
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = clean_text_columns(df)
    df = clean_date_columns(df)
    df = validate_numeric_columns(df)
    df = validate_business_rules(df)
    df = create_derived_columns(df)
    return df

def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned and transformed dataset to specified CSV destination."""
    df.to_csv(output_path, index=False)