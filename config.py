"""
Configuration settings for the Deep Research AI Agent System
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# === API Keys ===
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Check if the keys are loaded properly (optional, for debugging)
if not TAVILY_API_KEY or not GOOGLE_API_KEY:
    raise EnvironmentError("Missing API keys. Please check your .env file.")

# === LLM Parameters ===
DEFAULT_TEMPERATURE = 0.2
MAX_RESEARCH_ITERATIONS = 3
MAX_DRAFTING_ITERATIONS = 2

# === File Storage Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
RESEARCH_RESULTS_DIR = os.path.join(RESULTS_DIR, "research")
DRAFT_RESULTS_DIR = os.path.join(RESULTS_DIR, "drafts")

# === Ensure Results Directories Exist ===
os.makedirs(RESEARCH_RESULTS_DIR, exist_ok=True)
os.makedirs(DRAFT_RESULTS_DIR, exist_ok=True)
