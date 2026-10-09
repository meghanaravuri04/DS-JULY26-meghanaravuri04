"""KPI / analysis function tests using controlled fixtures."""
import pandas as pd
import pytest

from src.insurance_analysis import (
    calculate_total_policies, calculate_active_policies,
    calculate_total_claims, calculate_total_premium,
    calculate_claim_approval_rate, calculate_average_claim_amount,
    calculate_total_claim_amount, calculate_claim_rejection_rate,
    analyze_vehicle_claims,
)


@pytest.fixture
def tiny_data():
    return {
        "policies": pd.DataFrame({
            "policy_id": ["P1", "P2", "P3", "P4"],
            "premium_amount": [10000, 5000, 8000, 7000],
            "policy_status": ["Active", "Active", "Expired", "Cancelled"],
        }),
        "claims": pd.DataFrame({
            "claim_id": ["CL1", "CL2", "CL3"],
            "claim_amount": [1000, 2000, 3000],
            "claim_status": ["Approved", "Rejected", "Approved"],
        }),
    }


def test_calculate_total_policies(tiny_data):
    assert calculate_total_policies(tiny_data) == 4


def test_calculate_active_policies(tiny_data):
    assert calculate_active_policies(tiny_data) == 2


def test_calculate_total_claims(tiny_data):
    assert calculate_total_claims(tiny_data) == 3


def test_calculate_total_premium(tiny_data):
    assert calculate_total_premium(tiny_data) == 30000.0


def test_calculate_claim_approval_rate(tiny_data):
    # 2 approved / 3 total = 66.67%
    assert pytest.approx(calculate_claim_approval_rate(tiny_data), 0.01) == 66.67


def test_calculate_claim_rejection_rate(tiny_data):
    # 1 rejected / 3 total = 33.33%
    assert pytest.approx(calculate_claim_rejection_rate(tiny_data), 0.01) == 33.33


def test_calculate_total_claim_amount(tiny_data):
    assert calculate_total_claim_amount(tiny_data) == 6000.0


def test_calculate_average_claim_amount(tiny_data):
    assert calculate_average_claim_amount(tiny_data) == 2000.0


def test_analyze_vehicle_claims_joins_via_policy_id():
    data = {
        "claims": pd.DataFrame({
            "claim_id": ["CL1", "CL2"],
            "policy_id": ["P1", "P2"],
            "claim_amount": [1000, 2500],
        }),
        "policies": pd.DataFrame({
            "policy_id": ["P1", "P2"],
            "vehicle_id": ["V1", "V2"],
        }),
        "vehicles": pd.DataFrame({
            "vehicle_id": ["V1", "V2"],
            "vehicle_type": ["Sedan", "SUV"],
            "vehicle_make": ["Make A", "Make B"],
            "fuel_type": ["Petrol", "Diesel"],
            "vehicle_age": [4, 6],
        }),
    }

    result = analyze_vehicle_claims(data).set_index("vehicle_type")

    assert result.loc["Sedan", "total_claims"] == 1
    assert result.loc["Sedan", "total_claim_amount"] == 1000
    assert result.loc["SUV", "total_claims"] == 1
    assert result.loc["SUV", "total_claim_amount"] == 2500