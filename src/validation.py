"""Validation module for table structure, keys, ranges, and relationships."""
import pandas as pd
from src.logger import setup_logger, log_pipeline_step, log_error

logger = setup_logger()

REQUIRED_COLUMNS = {
    "customers": ["customer_id", "customer_name", "gender", "date_of_birth",
                  "age", "city", "state", "occupation"],
    "vehicles": ["vehicle_id", "customer_id", "vehicle_type", "vehicle_make",
                 "vehicle_model", "vehicle_year", "fuel_type", "vehicle_value"],
    "policies": ["policy_id", "customer_id", "vehicle_id", "policy_start_date",
                 "policy_end_date", "policy_type", "premium_amount",
                 "coverage_amount", "policy_status", "payment_frequency"],
    "claims": ["claim_id", "policy_id", "customer_id", "claim_date",
               "accident_date", "claim_type", "accident_location",
               "claim_amount", "claim_status", "approval_date",
               "settlement_date", "damage_severity"],
    "payments": ["payment_id", "claim_id", "policy_id", "payment_date",
                 "payment_amount", "payment_status", "payment_method"],
}

VALID_STATUSES = {
    "policy_status": {"Active", "Expired", "Cancelled", "Renewed"},
    "claim_status": {"Pending", "Approved", "Rejected", "Settled"},
    "damage_severity": {"Low", "Medium", "High"},
}


def _check_columns(df: pd.DataFrame, name: str) -> bool:
    missing = [c for c in REQUIRED_COLUMNS[name] if c not in df.columns]
    if missing:
        log_error(f"{name}: missing columns {missing}")
        return False
    return True


def validate_customers(df: pd.DataFrame) -> bool:
    """Validate customers table."""
    if not _check_columns(df, "customers"):
        return False
    if df["customer_id"].duplicated().any():
        log_error("customers: duplicate customer_id")
        return False
    if df["customer_id"].isna().any():
        log_error("customers: missing customer_id")
        return False
    return True


def validate_vehicles(df: pd.DataFrame) -> bool:
    """Validate vehicles table."""
    if not _check_columns(df, "vehicles"):
        return False
    if df["vehicle_id"].duplicated().any():
        log_error("vehicles: duplicate vehicle_id")
        return False
    if df["vehicle_id"].isna().any():
        log_error("vehicles: missing vehicle_id")
        return False
    return True


def validate_policies(df: pd.DataFrame) -> bool:
    """Validate policies table."""
    if not _check_columns(df, "policies"):
        return False
    if df["policy_id"].duplicated().any():
        log_error("policies: duplicate policy_id")
        return False
    if (df["premium_amount"] < 0).any():
        log_error("policies: negative premium")
        return False
    if not set(df["policy_status"].dropna().unique()).issubset(VALID_STATUSES["policy_status"]):
        log_error("policies: invalid policy_status values")
        return False
    return True


def validate_claims(df: pd.DataFrame) -> bool:
    """Validate claims table."""
    if not _check_columns(df, "claims"):
        return False
    if df["claim_id"].duplicated().any():
        log_error("claims: duplicate claim_id")
        return False
    if (df["claim_amount"] < 0).any():
        log_error("claims: negative claim_amount")
        return False
    if not set(df["claim_status"].dropna().unique()).issubset(VALID_STATUSES["claim_status"]):
        log_error("claims: invalid claim_status values")
        return False
    return True


def validate_payments(df: pd.DataFrame) -> bool:
    """Validate payments table."""
    if not _check_columns(df, "payments"):
        return False
    if df["payment_id"].duplicated().any():
        log_error("payments: duplicate payment_id")
        return False
    if (df["payment_amount"] < 0).any():
        log_error("payments: negative payment_amount")
        return False
    return True


def validate_relationships(data: dict) -> bool:
    """Validate foreign key relationships across tables."""
    ok = True
    policies, claims, payments = data["policies"], data["claims"], data["payments"]
    customers, vehicles = data["customers"], data["vehicles"]

    if not set(policies["customer_id"]).issubset(set(customers["customer_id"])):
        log_error("policies.customer_id not in customers")
        ok = False
    if not set(policies["vehicle_id"]).issubset(set(vehicles["vehicle_id"])):
        log_error("policies.vehicle_id not in vehicles")
        ok = False
    if not set(claims["policy_id"]).issubset(set(policies["policy_id"])):
        log_error("claims.policy_id not in policies")
        ok = False
    if not set(payments["claim_id"]).issubset(set(claims["claim_id"])):
        log_error("payments.claim_id not in claims")
        ok = False
    return ok


def validate_all_tables(data: dict) -> bool:
    """Run all validations and return True if everything passes."""
    log_pipeline_step("Starting validation of all tables")
    checks = [
        validate_customers(data["customers"]),
        validate_vehicles(data["vehicles"]),
        validate_policies(data["policies"]),
        validate_claims(data["claims"]),
        validate_payments(data["payments"]),
        validate_relationships(data),
    ]
    if all(checks):
        log_pipeline_step("All validations passed")
        return True
    log_error("One or more validation checks failed")
    return False