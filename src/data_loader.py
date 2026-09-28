import os
import pandas as pd

def check_file_exists(file_path: str) -> bool:
    """Check whether the specified file exists at the given path."""
    return os.path.exists(file_path)

def load_data(file_path: str) -> pd.DataFrame:
    """Load logistics CSV dataset into a Pandas DataFrame and normalize date columns."""
    if not check_file_exists(file_path):
        raise FileNotFoundError(f"File not found at path: {file_path}")

    df = pd.read_csv(file_path)
    for col in ['order_date', 'dispatch_date', 'expected_delivery_date', 'actual_delivery_date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df