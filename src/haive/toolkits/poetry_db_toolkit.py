from pydantic import BaseModel, Field
from typing import Optional, List
from langchain_core.tools import StructuredTool
import requests

BASE_URL = "https://poetrydb.org"

### --- Tool 1: Search Poems by Author --- ###
class AuthorSearchInput(BaseModel):
    author: str = Field(..., description="Name of the poet to search for")

def search_poems_by_author(author: str) -> List[dict]:
    url = f"{BASE_URL}/author/{author}"
    res = requests.get(url)
    res.raise_for_status()
    poems = res.json()
    return poems[:5]  # Return first 5 results

search_poems_by_author_tool = StructuredTool.from_function(
    func=search_poems_by_author,
    name="search_poems_by_author",
    description="Search for poems by a specific poet",
    args_schema=AuthorSearchInput
)


### --- Tool 2: Search Poem by Title --- ###
class TitleSearchInput(BaseModel):
    title: str = Field(..., description="Title of the poem")

def search_poem_by_title(title: str) -> dict:
    url = f"{BASE_URL}/title/{title}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()[0]  # Return first match

search_poem_by_title_tool = StructuredTool.from_function(
    func=search_poem_by_title,
    name="search_poem_by_title",
    description="Search for a poem using its title",
    args_schema=TitleSearchInput
)


### --- Tool 3: Get Random Poems --- ###
class RandomPoemInput(BaseModel):
    count: int = Field(..., description="Number of random poems to fetch")

def get_random_poems(count: int) -> List[dict]:
    url = f"{BASE_URL}/random/{count}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

get_random_poems_tool = StructuredTool.from_function(
    func=get_random_poems,
    name="get_random_poems",
    description="Get a number of random poems",
    args_schema=RandomPoemInput
)


### --- Tool 4: Search Poems by Line Fragment --- ###
class LineSearchInput(BaseModel):
    phrase: str = Field(..., description="Line or phrase to search for in poems")

def search_by_line_fragment(phrase: str) -> List[dict]:
    url = f"{BASE_URL}/lines/{phrase}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()[:3]

search_by_line_tool = StructuredTool.from_function(
    func=search_by_line_fragment,
    name="search_poems_by_line",
    description="Search for poems that contain a specific line or phrase",
    args_schema=LineSearchInput
)


### --- Toolkit Wrapper --- ###
def get_poetry_toolkit() -> List[StructuredTool]:
    return [
        search_poems_by_author_tool,
        search_poem_by_title_tool,
        get_random_poems_tool,
        search_by_line_tool
    ]