from typing import Optional
from pydantic import BaseModel, Field
import requests
from langchain.tools import StructuredTool


class GetProductInfoInput(BaseModel):
    barcode: str = Field(..., description="The barcode of the product to look up.")

def get_product_info(barcode: str) -> dict:
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error fetching product data: {response.status_code}")
    data = response.json()
    if "product" not in data:
        raise ValueError("No product data found.")
    return data["product"]

open_food_facts_tool = StructuredTool.from_function(
    func=get_product_info,
    name="get_open_food_facts_product",
    description="Use this tool to retrieve product data using a barcode from Open Food Facts.",
    args_schema=GetProductInfoInput,
)
