# tools/freetogame_toolkit.py

import requests
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain.tools import BaseToolkit, StructuredTool


BASE_URL = "https://www.freetogame.com/api"


class GetAllGamesInput(BaseModel):
    """Retrieve all free-to-play games, optionally filtered by platform, category, and sort order."""
    platform: Optional[str] = Field(None, description="Platform name, e.g. 'pc', 'browser'")
    category: Optional[str] = Field(None, description="Category/tag, e.g. 'shooter', 'mmorpg'")
    sort_by: Optional[str] = Field(None, description="Sort by one of: 'release-date', 'popularity', 'alphabetical', 'relevance'")


def get_all_games(input: GetAllGamesInput) -> List[dict]:
    params = {}
    if input.platform:
        params["platform"] = input.platform
    if input.category:
        params["category"] = input.category
    if input.sort_by:
        params["sort-by"] = input.sort_by
    response = requests.get(f"{BASE_URL}/games", params=params)
    response.raise_for_status()
    return response.json()


class GetGameDetailsInput(BaseModel):
    """Get detailed information about a specific game by ID."""
    game_id: int = Field(..., description="The game ID to retrieve.")


def get_game_details(input: GetGameDetailsInput) -> dict:
    response = requests.get(f"{BASE_URL}/game", params={"id": input.game_id})
    response.raise_for_status()
    return response.json()


class FilterGamesByTagsInput(BaseModel):
    """Filter games by multiple tags (dot-separated) and optional platform."""
    tag: str = Field(..., description="Dot-separated tag filter, e.g. '3d.mmorpg.fantasy.pvp'")
    platform: Optional[str] = Field(None, description="Platform name, e.g. 'pc', 'browser'")


def filter_games_by_tags(input: FilterGamesByTagsInput) -> List[dict]:
    params = {"tag": input.tag}
    if input.platform:
        params["platform"] = input.platform
    response = requests.get(f"{BASE_URL}/filter", params=params)
    response.raise_for_status()
    return response.json()


class FreeToGameToolkit(BaseToolkit):
    """LangChain toolkit for the FreeToGame API (Free-To-Play Games Database)."""

    def get_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(get_all_games),
            StructuredTool.from_function(get_game_details),
            StructuredTool.from_function(filter_games_by_tags),
        ]
