#!/usr/bin/env python3
"""
Dedicated web server module for the Deep Research AI Agent System
"""
from app import app

# This is the dedicated app runner file to avoid 
# circular import issues with the main.py file

if __name__ == "__main__":
    # Run the web server
    print("Starting web server on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
