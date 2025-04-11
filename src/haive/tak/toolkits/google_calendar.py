"""
Requires the credentials.json
"""

from langchain_google_community.calendar.toolkit import CalendarToolkit
from src.config.config import Config

import os
import sys
from langchain_google_community.gmail.toolkit import GmailToolkit

# Define the credentials file path
CREDENTIALS_FILE = "credentials.json"

# Check if the credentials file exists in the root directory
if not os.path.exists(CREDENTIALS_FILE):
    print(f"❌ Error: '{CREDENTIALS_FILE}' not found in the root directory.")
    print("🔹 Please ensure the credentials file is present before running the script.")
    sys.exit(1)  # Exit the program if credentials are missing

# Initialize the Gmail toolkit only if credentials exist
try:
    google_calendar_toolkit = CalendarToolkit().get_tools()
    print("✅ Google CalendarToolkit initialized successfully.")
except Exception as e:
    print(f"❌ Failed to initialize Google CalendarToolkit: {e}")


#print(google_calendar_tools)