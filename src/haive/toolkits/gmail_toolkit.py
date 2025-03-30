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
    gmail_toolkit = GmailToolkit().get_tools()
    print("✅ GmailToolkit initialized successfully.")
except Exception as e:
    print(f"❌ Failed to initialize GmailToolkit: {e}")
