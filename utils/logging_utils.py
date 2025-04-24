"""
Logging utility functions
"""
import logging
import os
import sys
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Set up logging configuration
    
    Args:
        log_level: Logging level (default: INFO)
        log_file: Optional path to log file
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create handlers
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)
    
    # File handler (if log_file provided)
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers,
        force=True
    )
    
    # Set logging levels for external libraries
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logging.info("Logging configured successfully")

def get_rotating_log_file():
    """
    Generate a log file path with timestamp
    
    Returns:
        Path to log file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, f"research_agent_{timestamp}.log")
