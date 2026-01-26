"""
Configuration file for ATIM project.
Store API keys and other configuration settings here.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Available models: gemini-2.0-flash (fast, free tier), gemini-2.5-flash, gemini-2.5-pro (more capable)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# SerpAPI Configuration
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

# Google Trends Configuration
TRENDS_GEO = "US"  # Default geographic region
TRENDS_TIMEFRAME = "today 3-m"  # Last 3 months

# Inventory Configuration
DEFAULT_REORDER_POINT = 100  # Minimum stock level before reorder
DEFAULT_LEAD_TIME_DAYS = 14  # Average lead time for new orders

# Season Mapping
CURRENT_SEASON = "Late Summer"  # Can be updated based on current date






