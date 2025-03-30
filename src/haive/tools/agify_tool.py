import requests
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool


class AgifyResponse(BaseModel):
    """Response from the Agify API"""
    name: str = Field(description="The name to estimate age for")
    age: int = Field(description="The estimated age of the name")
    count: int = Field(description="The number of people with the name in the country")
    country_id: Optional[str] = Field(description="The country code of the name")


def estimate_age(name: str, country_id: Optional[str] = None) -> AgifyResponse:
    url = "https://api.agify.io"
    params = {"name": name}
    if country_id:
        params["country_id"] = country_id
    response = requests.get(url, params=params)
    response.raise_for_status()
    return AgifyResponse(**response.json())




AgifyToolkit = [
    StructuredTool.from_function(
        func=estimate_age,
        name="estimate_age",
        description="Estimate age from a single first name, with optional country scope.",
    )
]
