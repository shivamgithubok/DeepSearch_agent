#!/usr/bin/env python3
"""
Main entry point for the AI Agent-based Deep Research System
"""
import os
import logging
from cli import run_cli
from app import app  # Import the app for Gunicorn

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    # Run the CLI
    run_cli()
