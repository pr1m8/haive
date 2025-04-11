from langchain.tools import StructuredTool, BaseToolkit
from typing import Optional
import requests
import os


# Environment configuration
FRED_API_KEY = os.getenv("FRED_API_KEY")
BASE_URL = "https://api.stlouisfed.org/fred"


# Helper function to call the FRED API
def fred_get(endpoint: str, params: dict) -> dict:
    params["api_key"] = FRED_API_KEY
    params["file_type"] = "json"
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    response.raise_for_status()
    return response.json()


# Core endpoint functions
def get_category(category_id: int) -> dict:
    return fred_get("category", {"category_id": category_id})

def get_category_children(category_id: int) -> dict:
    return fred_get("category/children", {"category_id": category_id})

def get_category_series(category_id: int) -> dict:
    return fred_get("category/series", {"category_id": category_id})

def get_series(series_id: str) -> dict:
    return fred_get("series", {"series_id": series_id})

def get_series_observations(series_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> dict:
    params = {"series_id": series_id}
    if start_date:
        params["observation_start"] = start_date
    if end_date:
        params["observation_end"] = end_date
    return fred_get("series/observations", params)


# LangChain-compatible toolkit
class FREDToolkit(BaseToolkit):
    def get_tools(self):
        return [
            StructuredTool.from_function(
                func=get_category,
                name="get_category",
                description="Get a FRED category by ID"
            ),
            StructuredTool.from_function(
                func=get_category_children,
                name="get_category_children",
                description="Get child categories for a FRED category"
            ),
            StructuredTool.from_function(
                func=get_category_series,
                name="get_category_series",
                description="List series in a FRED category"
            ),
            StructuredTool.from_function(
                func=get_series,
                name="get_series",
                description="Retrieve metadata for a FRED series"
            ),
            StructuredTool.from_function(
                func=get_series_observations,
                name="get_series_observations",
                description="Get FRED series observations. Optional start and end date (YYYY-MM-DD)."
            ),
        ]


# Usage
fred_toolkit = FREDToolkit()
tools = fred_toolkit.get_tools()
