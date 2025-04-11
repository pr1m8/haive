import os
from src.config.config import Config
from O365 import Account
from langchain_community.agent_toolkits import O365Toolkit
from langchain_community.tools.office365.events_search import O365SearchEvents

# 🔧 Required by Pydantic v2
O365SearchEvents.model_rebuild()

# 🔐 Validate environment variables
if not Config.AZURE_CLIENT_ID or not Config.AZURE_SECRET_ID:
    raise ValueError(
        "Error: The CLIENT_ID and CLIENT_SECRET environmental variables have not been set. "
        "Visit https://learn.microsoft.com/en-us/graph/auth/"
    )

# ✅ Initialize O365 Toolkit
toolkit = O365Toolkit(
    client_id=Config.AZURE_CLIENT_ID,
    client_secret=Config.AZURE_SECRET_ID,
    tenant_id=Config.AZURE_TENANT_ID,
    scopes=[
        "offline_access",
        "https://graph.microsoft.com/Calendars.Read",
        "https://graph.microsoft.com/Mail.Read",
        "https://graph.microsoft.com/User.Read"
    ],
)

tools = toolkit.get_tools()
print(f"✅ Loaded O365 tools: {[t.name for t in tools]}")
