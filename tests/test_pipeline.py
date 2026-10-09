"""Pipeline tests: loading, deduplication, derived columns, saving."""
import os
import pandas as pd
import pytest

from src.data_loader import load_table, load_all_data
from src.data_cleaner import (
    remove_duplicates, create_derived_columns,
    clean_data, save_cleaned_data,
)


# --------------------------- Fixtures ---------------------------
@pytest.fixture
def sample_policies():
    return pd.DataFrame({
        "policy_id": ["P1", "P2", "P2"],
        "customer_id": ["C1", "C2", "C2"],
        "vehicle_id": ["V1", "V2", "V2"],
        "policy_start_date": pd.to_datetime(["2023-01-01", "2023-02-01", "2023-02-01"]),
        "policy_end_date":   pd.to_datetime(["2024-01-01", "2024-02-01", "2024-02-01"]),
        "policy_type": ["Comprehensive", "Third-Party", "Third-Party"],
        "premium_amount": [12000, 5000, 5000],
        "coverage_amount": [500000, 200000, 200000],
        "policy_status": ["Active", "Expired", "Expired"],
        "payment_frequency": ["Annual", "Monthly", "Monthly"],
    })


@pytest.fixture
def sample_data(sample_policies):
    return {
        "customers": pd.DataFrame({
            "customer_id": ["C1", "C2"],
            "customer_name": ["Alice", "Bob"],
            "gender": ["Female", "Male"],
            "date_of_birth": pd.to_datetime(["1990-05-10", "1985-07-15"]),
            "age": [34, 39],
            "city": ["Pune", "Mumbai"],
            "state": ["Maharashtra", "Maharashtra"],
            "occupation": ["Engineer", "Doctor"],
        }),

        "vehicles": pd.DataFrame({
            "vehicle_id": ["V1", "V2"],
            "customer_id": ["C1", "C2"],
            "vehicle_type": ["Sedan", "Bike"],
            "vehicle_make": ["Honda", "Bajaj"],
            "vehicle_model": ["City", "Pulsar"],
            "vehicle_year": [2018, 2020],
            "fuel_type": ["Petrol", "Petrol"],
            "vehicle_value": [800000, 120000],
        }),

        "policies": sample_policies,

        "claims": pd.DataFrame({
            "claim_id": ["CL1", "CL2"],
            "policy_id": ["P1", "P2"],
            "customer_id": ["C1", "C2"],
            "vehicle_id": ["V1", "V2"],        # 👈 REQUIRED
            "claim_date": pd.to_datetime(["2023-06-01", "2023-08-01"]),
            "accident_date": pd.to_datetime(["2023-05-30", "2023-07-30"]),
            "claim_type": ["Accident", "Theft"],
            "accident_location": ["Pune", "Mumbai"],
            "claim_amount": [10000, 4000],
            "claim_status": ["Approved", "Rejected"],
            "approval_date": pd.to_datetime(["2023-06-05", "2023-08-07"]),
            "settlement_date": pd.to_datetime(["2023-06-15", "2023-08-20"]),
            "damage_severity": ["Low", "Medium"],
        }),

        "payments": pd.DataFrame({
            "payment_id": ["PAY1", "PAY2"],
            "claim_id": ["CL1", "CL2"],
            "policy_id": ["P1", "P2"],          # 👈 REQUIRED
            "payment_date": pd.to_datetime(["2023-06-16", "2023-08-21"]),
            "payment_amount": [9500, 3800],
            "payment_status": ["Paid", "Paid"],
            "payment_method": ["NEFT", "UPI"],
        }),
    }

# --------------------------- Tests ---------------------------
def test_load_table_returns_dataframe(tmp_path):
    """load_table should return a DataFrame from a valid CSV."""
    csv = tmp_path / "sample.csv"
    pd.DataFrame({"a": [1, 2], "b": [3, 4]}).to_csv(csv, index=False)
    df = load_table(str(csv))
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)


def test_load_all_data_reads_all_five_tables(tmp_path):
    """load_all_data should read all five required CSVs."""
    for name in ["customers", "vehicles", "policies", "claims", "payments"]:
        pd.DataFrame({"x": [1]}).to_csv(tmp_path / f"{name}.csv", index=False)
    data = load_all_data(str(tmp_path))
    assert set(data.keys()) == {"customers", "vehicles", "policies", "claims", "payments"}


def test_remove_duplicates(sample_data):
    """Duplicate policy row should be removed."""
    before = len(sample_data["policies"])
    out = remove_duplicates(sample_data)
    after = len(out["policies"])
    assert after == before - 1
    assert out["policies"]["policy_id"].duplicated().sum() == 0


def test_create_derived_columns_adds_expected(sample_data):
    """Derived columns must appear after create_derived_columns."""
    out = create_derived_columns(sample_data)
    assert "policy_duration_days" in out["policies"].columns
    assert "policy_active_flag" in out["policies"].columns
    assert "customer_age" in out["customers"].columns
    assert "vehicle_age" in out["vehicles"].columns
    assert "claim_processing_days" in out["claims"].columns
    assert "claim_settlement_days" in out["claims"].columns
    assert "claim_to_premium_ratio" in out["claims"].columns
    assert "paid_claim_ratio" in out["payments"].columns


def test_clean_data_runs_end_to_end(sample_data):
    """clean_data should return a dict with all five cleaned tables."""
    out = clean_data(sample_data)
    assert set(out.keys()) == {"customers", "vehicles", "policies", "claims", "payments"}
    # Duplicates removed
    assert out["policies"]["policy_id"].duplicated().sum() == 0


def test_save_cleaned_data_writes_files(tmp_path, sample_data):
    """save_cleaned_data must create one CSV per table."""
    cleaned = clean_data(sample_data)
    save_cleaned_data(cleaned, str(tmp_path))
    for name in ["customers", "vehicles", "policies", "claims", "payments"]:
        assert (tmp_path / f"{name}_cleaned.csv").exists()