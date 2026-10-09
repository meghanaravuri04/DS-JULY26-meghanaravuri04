"""
run_pipeline.py
---------------
Entry point. Run with:  python run_pipeline.py

Full pipeline:
    load -> validate -> clean -> save cleaned
"""

import sys
import time
from src.logger import setup_logger, log_pipeline_step, log_error
from src.data_loader import load_all_data
from src.validation import validate_all_tables
from src.data_cleaner import clean_data, save_cleaned_data

logger = setup_logger()


def run_pipeline() -> dict:
    """
    Execute the full data pipeline.

    Returns
    -------
    dict
        Cleaned tables keyed by name.
    """
    start = time.time()
    log_pipeline_step("=" * 60)
    log_pipeline_step("PIPELINE STARTED")
    log_pipeline_step("=" * 60)

    try:
        # 1. Load
        data = load_all_data("data/raw")

        # 2. Validate
        if not validate_all_tables(data):
            log_error("Validation failed — aborting pipeline")
            sys.exit(1)

        # 3. Clean
        data = clean_data(data)

        # 4. Save cleaned
        save_cleaned_data(data, "data/cleaned")

        elapsed = time.time() - start
        log_pipeline_step(f"PIPELINE COMPLETED in {elapsed:.2f}s")
        log_pipeline_step("=" * 60)
        return data

    except Exception as e:
        log_error(f"Pipeline crashed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()