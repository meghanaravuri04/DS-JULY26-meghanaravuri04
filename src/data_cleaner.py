"""Data cleaning, type enforcement, business rules, and derived columns."""
import os
import pandas as pd
import numpy as np
from src.logger import setup_logger, log_pipeline_step

logger = setup_logger()


def handle_missing_values(data: dict) -> dict:
    """Fill/drop missing values per business rules."""
    for name, df in data.items():
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].fillna("Unknown")
            elif pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
        data[name] = df
    log_pipeline_step("Missing values handled")
    return data


def remove_duplicates(data: dict) -> dict:
    """Remove full-row duplicates from each table."""
    for name, df in data.items():
        before = len(df)
        data[name] = df.drop_duplicates().reset_index(drop=True)
        log_pipeline_step(f"{name}: removed {before - len(data[name])} duplicate rows")
    return data


def clean_text_columns(data: dict) -> dict:
    """Strip whitespace and title-case text columns."""
    for name, df in data.items():
        for col in df.select_dtypes(include="str").columns:
            df[col] = df[col].astype(str).str.strip().str.title()
        data[name] = df
    log_pipeline_step("Text columns cleaned")
    return data


def clean_date_columns(data: dict) -> dict:
    """Convert known date columns to datetime."""
    date_cols = {
        "customers": ["date_of_birth"],
        "policies": ["policy_start_date", "policy_end_date"],
        "claims": ["claim_date", "accident_date", "approval_date", "settlement_date"],
        "payments": ["payment_date"],
    }
    for name, cols in date_cols.items():
        for col in cols:
            if col in data[name].columns:
                data[name][col] = pd.to_datetime(data[name][col], errors="coerce")
    log_pipeline_step("Date columns converted")
    return data


def validate_numeric_columns(data: dict) -> dict:
    """Ensure numeric columns are numeric; replace negatives where invalid."""
    numeric = {
        "policies": ["premium_amount", "coverage_amount"],
        "claims": ["claim_amount"],
        "payments": ["payment_amount"],
        "vehicles": ["vehicle_value", "vehicle_year"],
        "customers": ["age"],
    }
    for name, cols in numeric.items():
        for col in cols:
            if col in data[name].columns:
                data[name][col] = pd.to_numeric(data[name][col], errors="coerce")
    log_pipeline_step("Numeric columns validated")
    return data


def validate_business_rules(data: dict) -> dict:
    """Drop rows violating key business rules."""
    p = data["policies"]
    p = p[p["premium_amount"] > 0]
    p = p[p["policy_end_date"] >= p["policy_start_date"]]
    data["policies"] = p.reset_index(drop=True)

    c = data["claims"]
    c = c[c["claim_amount"] >= 0]
    data["claims"] = c.reset_index(drop=True)
    log_pipeline_step("Business rules enforced")
    return data


def create_derived_columns(data: dict) -> dict:
    """Create all required derived columns across tables."""
    today = pd.Timestamp.today()

    # customers
    c = data["customers"]
    if "date_of_birth" in c.columns:
        c["customer_age"] = ((today - c["date_of_birth"]).dt.days // 365).abs()
    data["customers"] = c

    # vehicles
    v = data["vehicles"]
    if "vehicle_year" in v.columns:
        v["vehicle_age"] = (today.year - v["vehicle_year"]).clip(lower=0)
    data["vehicles"] = v

    # policies
    p = data["policies"]
    p["policy_duration_days"] = (p["policy_end_date"] - p["policy_start_date"]).dt.days
    p["policy_active_flag"] = (p["policy_status"].str.lower() == "active").astype(int)
    data["policies"] = p

    # claims
    cl = data["claims"]
    cl["claim_processing_days"] = (cl["approval_date"] - cl["claim_date"]).dt.days
    cl["claim_settlement_days"] = (cl["settlement_date"] - cl["claim_date"]).dt.days
    cl["claim_processing_days"] = cl["claim_processing_days"].clip(lower=0)
    cl["claim_settlement_days"] = cl["claim_settlement_days"].clip(lower=0)
    data["claims"] = cl

    # merge to compute ratios on claims
    pol_small = p[["policy_id", "premium_amount", "coverage_amount", "policy_type"]]
    cl = cl.merge(pol_small, on="policy_id", how="left")
    cl["claim_to_premium_ratio"] = cl["claim_amount"] / cl["premium_amount"].replace(0, np.nan)
    cl["claim_to_coverage_ratio"] = cl["claim_amount"] / cl["coverage_amount"].replace(0, np.nan)
    data["claims"] = cl

    # paid claim ratio on payments
    pay = data["payments"]
    claim_amt = cl[["claim_id", "claim_amount"]]
    pay = pay.merge(claim_amt, on="claim_id", how="left")
    pay["paid_claim_ratio"] = pay["payment_amount"] / pay["claim_amount"].replace(0, np.nan)
    data["payments"] = pay

    log_pipeline_step("Derived columns created")
    return data


def clean_data(data: dict) -> dict:
    """Full cleaning pipeline for all tables."""
    log_pipeline_step("Running full cleaning pipeline")
    data = handle_missing_values(data)
    data = remove_duplicates(data)
    data = clean_text_columns(data)
    data = clean_date_columns(data)
    data = validate_numeric_columns(data)
    data = validate_business_rules(data)
    data = create_derived_columns(data)
    return data


def save_cleaned_data(data: dict, output_dir: str = "data/cleaned") -> None:
    """Persist cleaned tables to CSV."""
    os.makedirs(output_dir, exist_ok=True)
    for name, df in data.items():
        out = os.path.join(output_dir, f"{name}_cleaned.csv")
        df.to_csv(out, index=False)
        log_pipeline_step(f"Saved {out} | shape={df.shape}")