"""
Flask application runner for the Deep Research AI Agent System
"""
from app import app

# This file exists specifically to run the Flask app with gunicorn
# It imports the app object from app.py to be used by the server

if __name__ == "__main__":
    # Run the Flask application directly (for development)
    app.run(debug=True, host="0.0.0.0", port=5000)