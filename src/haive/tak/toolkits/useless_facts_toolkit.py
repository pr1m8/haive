import requests
from typing import Optional
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

BASE_URL = "https://uselessfacts.jsph.pl/api/v2/facts"

class FactInput(BaseModel):
    language: Optional[str] = Field(default="en", description="Language of the fact. Supports 'en' or 'de'.")

def get_random_fact(language: Optional[str] = "en") -> str:
    res = requests.get(f"{BASE_URL}/random", params={"language": language}, headers={"Accept": "application/json"})
    res.raise_for_status()
    return res.json().get("text", "No fact found.")

def get_todays_fact(language: Optional[str] = "en") -> str:
    res = requests.get(f"{BASE_URL}/today", params={"language": language}, headers={"Accept": "application/json"})
    res.raise_for_status()
    return res.json().get("text", "No fact found for today.")

get_random_fact_tool = StructuredTool.from_function(
    name="get_random_useless_fact",
    description="Get a random useless fact. Optionally specify the language ('en' or 'de').",
    func=get_random_fact,
    args_schema=FactInput,
)

get_todays_fact_tool = StructuredTool.from_function(
    name="get_todays_useless_fact",
    description="Get today's useless fact. Optionally specify the language ('en' or 'de').",
    func=get_todays_fact,
    args_schema=FactInput,
)

useless_facts_toolkit = [get_random_fact_tool, get_todays_fact_tool]
