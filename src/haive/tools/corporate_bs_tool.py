import requests
from pydantic import BaseModel
from langchain_core.tools import StructuredTool


class CorporateBS(BaseModel):
    phrase: str


def get_random_corporate_bs() -> CorporateBS:
    """Fetch a random corporate buzzword phrase."""
    res = requests.get("https://corporatebs-generator.sameerkumar.website/")
    res.raise_for_status()
    data = res.json()
    return CorporateBS(phrase=data["phrase"])


CorporateBSToolkit = [
    StructuredTool.from_function(
        func=get_random_corporate_bs,
        name="get_random_corporate_bs",
        description="Generate a random corporate buzzword phrase"
    )
]
