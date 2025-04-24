#!/usr/bin/env python3
"""
Flask server runner for the Deep Research AI Agent System
"""
from app import app

if __name__ == "__main__":
    print("Starting Flask server on port 5000...")
    app.run(debug=True, host="0.0.0.0", port=5000)