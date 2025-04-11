import os
import requests
from typing import List, Optional
from langchain.tools import StructuredTool, BaseToolkit


def get_openaq_location(location_id: int, api_key: Optional[str] = None) -> dict:
    """Fetches OpenAQ location details by location ID."""
    api_key = api_key or os.getenv("OPENAQ_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAQ API key. Set OPENAQ_API_KEY env variable or pass explicitly.")

    url = f"https://api.openaq.org/v3/locations/{location_id}"
    headers = {"X-API-Key": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


openaq_location_tool = StructuredTool.from_function(
    name="get_openaq_location_by_id",
    description="Fetch air quality station details from OpenAQ by location ID. Requires an API key.",
    func=get_openaq_location,
)