from typing import Optional, List
import requests
from pydantic.v1 import BaseModel, Field
from langchain.tools import StructuredTool
from langchain.agents import Tool

# Schema for querying card info
class GetCardInfoInput(BaseModel):
    name: Optional[str] = Field(None, description="Exact card name")
    fname: Optional[str] = Field(None, description="Fuzzy search by name fragment")
    archetype: Optional[str] = Field(None, description="Card archetype, e.g. Blue-Eyes")
    attribute: Optional[str] = Field(None, description="Card attribute, e.g. DARK, LIGHT")
    race: Optional[str] = Field(None, description="Card race/type, e.g. Warrior, Dragon")
    level: Optional[int] = Field(None, description="Level or rank of the card")
    cardset: Optional[str] = Field(None, description="Card set, e.g. Metal Raiders")
    format: Optional[str] = Field(None, description="Card format, e.g. TCG, Speed Duel")
    misc: Optional[bool] = Field(False, description="Whether to include additional metadata")

def get_card_info(input_data: GetCardInfoInput):
    base_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    params = {k: v for k, v in input_data.dict().items() if v is not None}
    if input_data.misc:
        params["misc"] = "yes"
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

# Main card lookup tool
card_info_tool = StructuredTool.from_function(
    name="get_yugioh_card_info",
    description="Retrieve detailed Yu-Gi-Oh! card info using name, archetype, attribute, level, etc.",
    args_schema=GetCardInfoInput,
    func=get_card_info,
)

# Simple REST endpoints
def get_card_sets():
    return requests.get("https://db.ygoprodeck.com/api/v7/cardsets.php").json()

def get_archetypes():
    return requests.get("https://db.ygoprodeck.com/api/v7/archetypes.php").json()

def get_random_card():
    return requests.get("https://db.ygoprodeck.com/api/v7/randomcard.php").json()

def get_database_version():
    return requests.get("https://db.ygoprodeck.com/api/v7/checkDBVer.php").json()

# Toolkit
yugioh_api_toolkit = [
    card_info_tool,
    Tool(name="get_yugioh_card_sets", func=get_card_sets, description="Get all Yu-Gi-Oh! card sets"),
    Tool(name="get_yugioh_archetypes", func=get_archetypes, description="Get all Yu-Gi-Oh! archetypes"),
    Tool(name="get_random_yugioh_card", func=get_random_card, description="Get a random Yu-Gi-Oh! card"),
    Tool(name="get_yugioh_database_version", func=get_database_version, description="Check the Yu-Gi-Oh! database version"),
]
