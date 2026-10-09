"""Tests for dashboard business recommendations."""

import pandas as pd

from src.insights import generate_business_recommendations


def test_generate_business_recommendations_returns_dashboard_card_fields():
    data = {
        "claims": pd.DataFrame({
            "claim_status": ["Pending", "Rejected", "Rejected", "Approved"],
            "claim_to_premium_ratio": [1.2, 1.5, 0.8, 1.1],
            "claim_settlement_days": [10, 45, 60, 20],
            "damage_severity": ["High", "High", "Medium", "Low"],
        }),
        "policies": pd.DataFrame({
            "policy_status": ["Expired", "Expired", "Active", "Active"],
        }),
    }

    cards = generate_business_recommendations(data)

    assert cards
    assert all(
        set(card) == {"PATTERN", "EVIDENCE", "BUSINESS_MEANING", "RECOMMENDATION"}
        for card in cards
    )
    assert any("pending" in card["PATTERN"].casefold() for card in cards)
    assert any("rejection" in card["PATTERN"].casefold() for card in cards)
    assert any("settle" in card["PATTERN"].casefold() for card in cards)
    assert any("severity" in card["PATTERN"].casefold() for card in cards)
    assert any("expired" in card["PATTERN"].casefold() for card in cards)


def test_generate_business_recommendations_handles_empty_data():
    data = {
        "claims": pd.DataFrame(),
        "policies": pd.DataFrame(),
    }

    assert generate_business_recommendations(data) == []


def test_generate_business_recommendations_skips_missing_metrics():
    data = {
        "claims": pd.DataFrame({"claim_amount": [100, 200]}),
        "policies": pd.DataFrame({"premium_amount": [1000]}),
    }

    assert generate_business_recommendations(data) == []
