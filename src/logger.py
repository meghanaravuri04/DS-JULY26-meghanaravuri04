"""
Centralized logging configuration for the project.
All modules must use these functions instead of print().
"""
import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")

_logger_initialized = False


def setup_logger(name: str = "motor_insurance") -> logging.Logger:
    """Configure and return a logger writing to file + console."""
    global _logger_initialized
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if _logger_initialized:
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.propagate = False
    _logger_initialized = True
    return logger


def log_pipeline_step(message: str) -> None:
    """Log a pipeline stage message."""
    setup_logger().info(f"[PIPELINE] {message}")


def log_error(message: str) -> None:
    """Log an error message (never include secrets/credentials)."""
    setup_logger().error(f"[ERROR] {message}")