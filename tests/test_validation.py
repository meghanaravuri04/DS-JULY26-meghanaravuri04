"""Validation tests for column/relationship checks."""
import pandas as pd
import pytest

from src.validation import (
    validate_customers, validate_policies, validate_claims,
    validate_relationships, validate_all_tables,
)


@pytest.fixture
def valid_data():
    return {
        "customers": pd.DataFrame({
            "customer_id": ["C1", "C2"],
            "customer_name": ["A", "B"],
            "gender": ["M", "F"],
            "date_of_birth": pd.to_datetime(["1990-01-01", "1988-05-05"]),
            "age": [34, 36],
            "city": ["Pune", "Mumbai"],
            "state": ["MH", "MH"],
            "occupation": ["Eng", "Doc"],
        }),
        "vehicles": pd.DataFrame({
            "vehicle_id": ["V1", "V2"],
            "customer_id": ["C1", "C2"],
            "vehicle_type": ["Car", "Bike"],
            "vehicle_make": ["Honda", "Bajaj"],
            "vehicle_model": ["City", "Pulsar"],
            "vehicle_year": [2018, 2020],
            "fuel_type": ["Petrol", "Petrol"],
            "vehicle_value": [800000, 120000],
        }),
        "policies": pd.DataFrame({
            "policy_id": ["P1", "P2"],
            "customer_id": ["C1", "C2"],
            "vehicle_id": ["V1", "V2"],
            "policy_start_date": pd.to_datetime(["2023-01-01", "2023-02-01"]),
            "policy_end_date":   pd.to_datetime(["2024-01-01", "2024-02-01"]),
            "policy_type": ["Comprehensive", "Third-Party"],
            "premium_amount": [12000, 5000],
            "coverage_amount": [500000, 200000],
            "policy_status": ["Active", "Expired"],
            "payment_frequency": ["Annual", "Monthly"],
        }),
        "claims": pd.DataFrame({
            "claim_id": ["CL1", "CL2"],
            "policy_id": ["P1", "P2"],
            "customer_id": ["C1", "C2"],
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
            "policy_id": ["P1", "P2"],
            "payment_date": pd.to_datetime(["2023-06-16", "2023-08-21"]),
            "payment_amount": [9500, 3800],
            "payment_status": ["Paid", "Paid"],
            "payment_method": ["NEFT", "UPI"],
        }),
    }


def test_validate_customers(valid_data):
    assert validate_customers(valid_data["customers"]) is True


def test_validate_policies(valid_data):
    assert validate_policies(valid_data["policies"]) is True


def test_validate_claims(valid_data):
    assert validate_claims(valid_data["claims"]) is True


def test_validate_relationships(valid_data):
    assert validate_relationships(valid_data) is True


def test_validate_all_tables(valid_data):
    assert validate_all_tables(valid_data) is True


def test_validate_customers_missing_column():
    """Missing a required column must return False."""
    df = pd.DataFrame({"customer_id": ["C1"]})  # missing many columns
    assert validate_customers(df) is False


def test_validate_policies_bad_status(valid_data):
    """Invalid policy_status value should fail validation."""
    d = {k: v.copy() for k, v in valid_data.items()}
    d["policies"].loc[0, "policy_status"] = "INVALID"
    assert validate_policies(d["policies"]) is False