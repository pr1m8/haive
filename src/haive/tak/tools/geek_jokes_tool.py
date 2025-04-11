import requests
from typing import Optional
from langchain.tools import StructuredTool, BaseToolkit
from pydantic import BaseModel, Field


class GetGeekJokeInput(BaseModel):
    """No input required, but kept for LangChain compatibility."""
    dummy: Optional[str] = Field(None, description="Unused input; the joke requires no input.")


def get_geek_joke(_: GetGeekJokeInput) -> str:
    """Fetch a random geek/programming joke from the Geek Jokes API."""
    url = "https://geek-jokes.sameerkumar.website/api?format=json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("joke", "No joke found.")


get_geek_joke_tool = StructuredTool.from_function(
    name="get_geek_joke",
    description="Fetch a random geek or programming-related joke from the Geek Jokes API",
    func=get_geek_joke,
    args_schema=GetGeekJokeInput
)


