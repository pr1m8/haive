import requests
from typing import List, Optional
from pydantic import BaseModel
from langchain_core.tools import StructuredTool


class Joke(BaseModel):
    id: str
    icon_url: str
    value: str
    url: Optional[str] = None


def get_random_joke() -> Joke:
    res = requests.get("https://api.chucknorris.io/jokes/random")
    res.raise_for_status()
    return Joke(**res.json())


def get_random_joke_by_category(category: str) -> Joke:
    res = requests.get(f"https://api.chucknorris.io/jokes/random?category={category}")
    res.raise_for_status()
    return Joke(**res.json())


def get_available_categories() -> List[str]:
    res = requests.get("https://api.chucknorris.io/jokes/categories")
    res.raise_for_status()
    return res.json()


def search_jokes(query: str) -> List[Joke]:
    res = requests.get(f"https://api.chucknorris.io/jokes/search?query={query}")
    res.raise_for_status()
    data = res.json()
    return [Joke(**joke) for joke in data.get("result", [])]


ChuckNorrisToolkit = [
    StructuredTool.from_function(
        func=get_random_joke,
        name="get_random_chuck_joke",
        description="Get a random Chuck Norris joke"
    ),
    StructuredTool.from_function(
        func=get_random_joke_by_category,
        name="get_chuck_joke_by_category",
        description="Get a random Chuck Norris joke from a specified category"
    ),
    StructuredTool.from_function(
        func=get_available_categories,
        name="get_chuck_joke_categories",
        description="Get a list of all available joke categories"
    ),
    StructuredTool.from_function(
        func=search_jokes,
        name="search_chuck_jokes",
        description="Search for Chuck Norris jokes matching a text query"
    ),
]
