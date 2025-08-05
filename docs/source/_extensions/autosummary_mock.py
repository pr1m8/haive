"""Mock problematic imports for autosummary."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

# Create mock modules for problematic imports
mock_modules = [
    "langchain_google_vertexai",
    "langchain_cerebras",
    "langchain_cohere",
    "langchain_ai21",
    "nlpcloud",
    "elevenlabs",
    "jinaai",
    "asknews",
    "azure.identity",
    "o365",
    "semanticscholar",
    "python_steam_api",
    "wolframalpha",
    "stackapi",
    "praw",
    "pyowm",
    "pygithub",
    "google_auth_oauthlib",
    "googleapiclient",
    "amadeus",
    "atlassian",
    "slack_sdk",
    "googlemaps",
    "gradio_tools",
    "google.generativeai",
    "vertexai",
]

for module in mock_modules:
    sys.modules[module] = MagicMock()

# Also mock some specific classes that cause issues
sys.modules["haive.agents.conversation.directed.state"] = MagicMock()
sys.modules["haive.agents.conversation.directed.state"].DirectedConversationState = MagicMock
