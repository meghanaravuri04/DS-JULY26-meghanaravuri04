"""Data loading module for raw motor insurance tables."""
import os
import pandas as pd
from src.logger import setup_logger, log_pipeline_step, log_error

logger = setup_logger()

REQUIRED_FILES = {
    "customers": "customers.csv",
    "vehicles": "vehicles.csv",
    "policies": "policies.csv",
    "claims": "claims.csv",
    "payments": "payments.csv",
}


def check_file_exists(file_path: str) -> bool:
    """Return True if file exists, else raise FileNotFoundError."""
    if not os.path.isfile(file_path):
        log_error(f"File not found: {file_path}")
        raise FileNotFoundError(f"Missing required file: {file_path}")
    return True


def load_table(file_path: str) -> pd.DataFrame:
    """Load a single CSV table."""
    check_file_exists(file_path)
    df = pd.read_csv(file_path)
    log_pipeline_step(f"Loaded {os.path.basename(file_path)} -> shape {df.shape}")
    return df


def load_all_data(data_dir: str = "data/raw") -> dict:
    """Load all standard tables and return as dict of DataFrames."""
    log_pipeline_step(f"Loading all tables from {data_dir}")
    data = {}
    for key, fname in REQUIRED_FILES.items():
        data[key] = load_table(os.path.join(data_dir, fname))
    return data