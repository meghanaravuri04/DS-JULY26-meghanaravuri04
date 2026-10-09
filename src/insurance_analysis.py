"""Business KPI calculations for motor insurance portfolio."""
import pandas as pd
from src.logger import setup_logger

logger = setup_logger()


# ---------- Portfolio ----------
def calculate_total_customers(data):   return data["customers"]["customer_id"].nunique()
def calculate_total_policies(data):    return data["policies"]["policy_id"].nunique()
def calculate_active_policies(data):
    return (data["policies"]["policy_status"].str.lower() == "active").sum()
def calculate_expired_policies(data):
    return (data["policies"]["policy_status"].str.lower() == "expired").sum()
def calculate_cancelled_policies(data):
    return (data["policies"]["policy_status"].str.lower() == "cancelled").sum()
def calculate_renewed_policies(data):
    return (data["policies"]["policy_status"].str.lower() == "renewed").sum()


# ---------- Premium ----------
def calculate_total_premium(data):     return float(data["policies"]["premium_amount"].sum())
def calculate_average_premium(data):   return float(data["policies"]["premium_amount"].mean())
def calculate_average_coverage(data):  return float(data["policies"]["coverage_amount"].mean())
def calculate_premium_by_policy_type(data):
    return data["policies"].groupby("policy_type")["premium_amount"].sum().sort_values(ascending=False)


# ---------- Claims ----------
def calculate_total_claims(data):      return data["claims"]["claim_id"].nunique()
def calculate_approved_claims(data):
    return (data["claims"]["claim_status"].str.lower() == "approved").sum()
def calculate_rejected_claims(data):
    return (data["claims"]["claim_status"].str.lower() == "rejected").sum()
def calculate_pending_claims(data):
    return (data["claims"]["claim_status"].str.lower() == "pending").sum()
def calculate_total_claim_amount(data):    return float(data["claims"]["claim_amount"].sum())
def calculate_average_claim_amount(data):  return float(data["claims"]["claim_amount"].mean())
def calculate_claim_approval_rate(data):
    total = calculate_total_claims(data)
    return 0.0 if total == 0 else calculate_approved_claims(data) / total * 100
def calculate_claim_rejection_rate(data):
    total = calculate_total_claims(data)
    return 0.0 if total == 0 else calculate_rejected_claims(data) / total * 100


# ---------- Settlement ----------
def calculate_average_claim_processing_days(data):
    return float(data["claims"]["claim_processing_days"].dropna().mean())
def calculate_average_claim_settlement_days(data):
    return float(data["claims"]["claim_settlement_days"].dropna().mean())
def calculate_total_payment_amount(data):   return float(data["payments"]["payment_amount"].sum())
def calculate_average_payment_amount(data): return float(data["payments"]["payment_amount"].mean())


# ---------- Ratios ----------
def calculate_claim_to_premium_ratio(data):
    return float(data["claims"]["claim_to_premium_ratio"].dropna().mean())
def calculate_claim_to_coverage_ratio(data):
    return float(data["claims"]["claim_to_coverage_ratio"].dropna().mean())
def calculate_paid_claim_ratio(data):
    return float(data["payments"]["paid_claim_ratio"].dropna().mean())


# ---------- Customer / Vehicle ----------
def analyze_customer_claims(data):
    cl = data["claims"].merge(
        data["customers"][["customer_id", "customer_age", "gender", "occupation"]],
        on="customer_id", how="left")
    cl["age_group"] = pd.cut(cl["customer_age"],
                             bins=[0, 25, 35, 45, 55, 65, 120],
                             labels=["<25", "25-34", "35-44", "45-54", "55-64", "65+"])
    return cl.groupby("age_group", observed=True).agg(
        total_claims=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        avg_claim_amount=("claim_amount", "mean"),
    ).reset_index()


def analyze_customer_premium(data):
    p = data["policies"].merge(
        data["customers"][["customer_id", "customer_age", "gender"]],
        on="customer_id", how="left")
    p["age_group"] = pd.cut(p["customer_age"],
                            bins=[0, 25, 35, 45, 55, 65, 120],
                            labels=["<25", "25-34", "35-44", "45-54", "55-64", "65+"])
    return p.groupby("age_group", observed=True)["premium_amount"].agg(
        ["count", "sum", "mean"]).reset_index()


def merge_claims_with_vehicle_data(data):
    """Join claims to vehicle attributes through their related policies."""
    claim_policies = data["policies"][["policy_id", "vehicle_id"]]
    claims = data["claims"].merge(claim_policies, on="policy_id", how="left")
    return claims.merge(
        data["vehicles"][["vehicle_id", "vehicle_type", "vehicle_make",
                          "fuel_type", "vehicle_age"]],
        on="vehicle_id", how="left", suffixes=("", "_vehicle"))


def analyze_vehicle_claims(data):
    cl = merge_claims_with_vehicle_data(data)
    return cl.groupby("vehicle_type").agg(
        total_claims=("claim_id", "count"),
        total_claim_amount=("claim_amount", "sum"),
        avg_claim_amount=("claim_amount", "mean"),
    ).reset_index().sort_values("total_claim_amount", ascending=False)


def analyze_vehicle_risk_patterns(data):
    cl = data["claims"]
    return cl.groupby("damage_severity").agg(
        claims=("claim_id", "count"),
        avg_claim_amount=("claim_amount", "mean"),
        avg_settlement_days=("claim_settlement_days", "mean"),
    ).reset_index()


# ---------- Business ----------
def analyze_claim_type(data):
    return data["claims"].groupby("claim_type").agg(
        count=("claim_id", "count"),
        total_amount=("claim_amount", "sum"),
        avg_amount=("claim_amount", "mean"),
    ).reset_index().sort_values("count", ascending=False)


def analyze_claim_status(data):
    return data["claims"]["claim_status"].value_counts().reset_index().rename(
        columns={"index": "claim_status", "claim_status": "count"})


def analyze_policy_type(data):
    return data["policies"].groupby("policy_type").agg(
        policies=("policy_id", "count"),
        total_premium=("premium_amount", "sum"),
        avg_premium=("premium_amount", "mean"),
    ).reset_index().sort_values("total_premium", ascending=False)