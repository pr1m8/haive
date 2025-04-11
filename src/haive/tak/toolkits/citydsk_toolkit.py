from typing import Optional, List
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from langchain.tools.base import BaseToolkit
import requests

# --- Linked Data Tool ---

class CitySDKLinkedDataQueryInput(BaseModel):
    query: str = Field(..., description="SPARQL query to send to the CitySDK Linked Data endpoint.")

def run_citysdk_linkeddata_query(query: str) -> dict:
    endpoint = "https://citysdk.dm.fhnw.ch/sparql"
    headers = {"Accept": "application/sparql-results+json"}
    response = requests.get(endpoint, params={"query": query}, headers=headers)
    response.raise_for_status()
    return response.json()

citysdk_linked_data_tool = StructuredTool.from_function(
    func=run_citysdk_linkeddata_query,
    name="citysdk_linked_data_query",
    description="Send a SPARQL query to the CitySDK Linked Data API to retrieve structured city information.",
    args_schema=CitySDKLinkedDataQueryInput,
)

# --- Tourism Tool ---

class CitySDKTourismPOIInput(BaseModel):
    bbox: Optional[str] = Field(
        None,
        description="Bounding box (e.g., '24.9384,60.1695,24.9500,60.1750') to filter POIs geographically."
    )
    city: Optional[str] = Field(None, description="Optional city to filter POIs.")

def get_tourism_pois(bbox: Optional[str] = None, city: Optional[str] = None) -> dict:
    endpoint = "https://tourism-api.citysdk.cm-lisboa.pt/resources/pois"
    params = {}
    if bbox:
        params["bbox"] = bbox
    if city:
        params["city"] = city
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json()

citysdk_tourism_poi_tool = StructuredTool.from_function(
    func=get_tourism_pois,
    name="citysdk_tourism_poi_query",
    description="Retrieve Points of Interest from the CitySDK Tourism API using a bounding box or city filter.",
    args_schema=CitySDKTourismPOIInput,
)

# --- Toolkit ---

class CitySDKToolkit(BaseToolkit):
    def get_tools(self) -> List[StructuredTool]:
        return [citysdk_linked_data_tool, citysdk_tourism_poi_tool]
