from langchain.tools import StructuredTool, BaseToolkit
from pydantic import BaseModel, Field
from typing import List
import requests

class FruitNameInput(BaseModel):
    name: str = Field(..., description="Name of the fruit to retrieve data for")

def get_fruit_info(input: FruitNameInput) -> dict:
    response = requests.get(f"https://www.fruityvice.com/api/fruit/{input.name.lower()}")
    if response.status_code == 404:
        return {"error": f"Fruit '{input.name}' not found"}
    response.raise_for_status()
    return response.json()

fruit_lookup_tool = StructuredTool.from_function(
    name="get_fruit_info",
    description="Fetch nutrition and info about a specific fruit using its name from Fruityvice API",
    func=get_fruit_info
)

