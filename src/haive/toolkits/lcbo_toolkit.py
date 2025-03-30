from langchain.tools import StructuredTool, BaseToolkit
from typing import Optional, List
import requests
from pydantic import BaseModel, Field

# --- Tool to fetch a product by ID ---
class GetLCBOProductInput(BaseModel):
    product_id: int = Field(..., description="LCBO product ID")

def get_lcbo_product(product_id: int) -> dict:
    url = f"https://lcboapi.com/products/{product_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

get_product_tool = StructuredTool.from_function(
    name="get_lcbo_product_by_id",
    description="Fetch detailed info for a product using its LCBO product ID",
    func=get_lcbo_product,
    args_schema=GetLCBOProductInput
)

# --- Tool to search products ---
class SearchLCBOProductsInput(BaseModel):
    query: str = Field(..., description="Search query string")
    page: Optional[int] = Field(1, description="Page number of results")
    per_page: Optional[int] = Field(10, description="Number of results per page")

def search_lcbo_products(query: str, page: int = 1, per_page: int = 10) -> dict:
    url = "https://lcboapi.com/products"
    params = {"q": query, "page": page, "per_page": per_page}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

search_products_tool = StructuredTool.from_function(
    name="search_lcbo_products",
    description="Search for LCBO products by keyword, name, etc.",
    func=search_lcbo_products,
    args_schema=SearchLCBOProductsInput
)

# --- Toolkit wrapper ---
class LCBOApiToolkit(BaseToolkit):
    def get_tools(self) -> List[StructuredTool]:
        return [get_product_tool, search_products_tool]
