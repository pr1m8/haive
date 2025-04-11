from typing import Optional, List
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool, BaseToolkit
import requests

GRAPHQL_ENDPOINT = "https://rickandmortyapi.com/graphql"
REST_BASE_URL = "https://rickandmortyapi.com/api"


# --------------------- REST Tools ---------------------

class GetCharacterByIDInput(BaseModel):
    id: int = Field(..., description="The ID of the character.")

def get_character_by_id(id: int) -> dict:
    url = f"{REST_BASE_URL}/character/{id}"
    return requests.get(url).json()

get_character_tool = StructuredTool.from_function(
    name="get_rick_and_morty_character_by_id",
    description="Get Rick and Morty character by ID using the REST API.",
    func=get_character_by_id,
    args_schema=GetCharacterByIDInput
)


class FilterCharactersInput(BaseModel):
    name: Optional[str] = Field(None, description="Filter characters by name.")
    status: Optional[str] = Field(None, description="alive, dead, or unknown")
    species: Optional[str] = Field(None, description="Filter characters by species.")
    gender: Optional[str] = Field(None, description="male, female, genderless, unknown")

def filter_characters(name=None, status=None, species=None, gender=None) -> dict:
    params = {
        "name": name,
        "status": status,
        "species": species,
        "gender": gender
    }
    params = {k: v for k, v in params.items() if v}
    url = f"{REST_BASE_URL}/character"
    return requests.get(url, params=params).json()

filter_characters_tool = StructuredTool.from_function(
    name="filter_rick_and_morty_characters",
    description="Filter Rick and Morty characters using the REST API with optional parameters.",
    func=filter_characters,
    args_schema=FilterCharactersInput
)


# --------------------- GraphQL Tools ---------------------

class GraphQLCharactersQueryInput(BaseModel):
    name: Optional[str] = Field(None, description="Character name to filter")
    page: Optional[int] = Field(None, description="Page number")

def graphql_characters_query(name: Optional[str] = None, page: Optional[int] = None) -> dict:
    query = """
    query ($page: Int, $name: String) {
      characters(page: $page, filter: { name: $name }) {
        info {
          count
          pages
          next
          prev
        }
        results {
          id
          name
          status
          species
          gender
        }
      }
    }
    """
    variables = {"page": page, "name": name}
    response = requests.post(GRAPHQL_ENDPOINT, json={"query": query, "variables": variables})
    return response.json()

graphql_characters_tool = StructuredTool.from_function(
    name="graphql_query_rick_and_morty_characters",
    description="Query Rick and Morty characters using GraphQL endpoint with optional page and name filter.",
    func=graphql_characters_query,
    args_schema=GraphQLCharactersQueryInput
)


class GraphQLLocationByIDInput(BaseModel):
    id: int = Field(..., description="Location ID")

def graphql_location_by_id(id: int) -> dict:
    query = """
    query ($id: ID!) {
      location(id: $id) {
        id
        name
        type
        dimension
      }
    }
    """
    response = requests.post(GRAPHQL_ENDPOINT, json={"query": query, "variables": {"id": id}})
    return response.json()

graphql_location_tool = StructuredTool.from_function(
    name="graphql_query_rick_and_morty_location",
    description="Query a specific location by ID from the Rick and Morty GraphQL API.",
    func=graphql_location_by_id,
    args_schema=GraphQLLocationByIDInput
)


# --------------------- Toolkit ---------------------

class RickAndMortyToolkit(BaseToolkit):
    """Toolkit for Rick and Morty API."""
    def get_tools(self) -> List[StructuredTool]:
        return [
            get_character_tool,
            filter_characters_tool,
            graphql_characters_tool,
            graphql_location_tool
        ]
