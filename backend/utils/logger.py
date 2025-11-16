"""
Logging configuration for Fashion Try-On Backend
"""

import logging
import sys
from pathlib import Path

# Create logs directory
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create formatters
formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(log_dir / "app.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

# Error file handler
error_handler = logging.FileHandler(log_dir / "error.log")
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler, error_handler]
)

# Create logger instance
logger = logging.getLogger("fashion_tryon")


def get_logger(name: str = "fashion_tryon") -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)
