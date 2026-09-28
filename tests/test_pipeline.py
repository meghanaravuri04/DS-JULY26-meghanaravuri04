import os
import pandas as pd
import pytest
from src.data_loader import load_data
from src.data_cleaner import clean_data, save_cleaned_data, remove_duplicates, create_derived_columns
from src.business_analysis import calculate_total_orders, calculate_on_time_percentage

RAW_PATH = os.path.join('data', 'raw', 'logistics_data.csv')
CLEANED_PATH = os.path.join('data', 'cleaned', 'test_cleaned.csv')

def test_load_data():
    df = load_data(RAW_PATH)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

def test_remove_duplicates():
    df = load_data(RAW_PATH)
    dedup = remove_duplicates(df)
    assert len(dedup) <= len(df)

def test_create_derived_columns():
    df = load_data(RAW_PATH)
    df_derived = create_derived_columns(df)
    assert 'total_logistics_cost' in df_derived.columns
    assert 'cost_per_km' in df_derived.columns
    assert 'on_time_flag' in df_derived.columns

def test_clean_data():
    df = load_data(RAW_PATH)
    df_clean = clean_data(df)
    assert df_clean['order_id'].isnull().sum() == 0

def test_calculate_total_orders():
    df = load_data(RAW_PATH)
    total = calculate_total_orders(df)
    assert total > 0

def test_calculate_on_time_percentage():
    df = load_data(RAW_PATH)
    df_clean = clean_data(df)
    pct = calculate_on_time_percentage(df_clean)
    assert 0.0 <= pct <= 100.0

def test_save_cleaned_data():
    df = load_data(RAW_PATH)
    df_clean = clean_data(df)
    save_cleaned_data(df_clean, CLEANED_PATH)
    assert os.path.exists(CLEANED_PATH)
    if os.path.exists(CLEANED_PATH):
        os.remove(CLEANED_PATH)