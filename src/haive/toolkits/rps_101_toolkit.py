from typing import List, Optional
from pydantic import BaseModel, Field
import requests
from langchain.tools import StructuredTool, BaseToolkit

BASE_URL = "https://rps101.pythonanywhere.com/api/v1"

# Tool 1: Get All RPS-101 Objects
def _get_all_rps101_objects() -> List[str]:
    response = requests.get(f"{BASE_URL}/objects/all")
    response.raise_for_status()
    return response.json()

get_all_rps101_objects = StructuredTool.from_function(
    name="get_all_rps101_objects",
    description="Get a list of all RPS-101 objects (e.g. Rock, Paper, Scissors, Nuke, etc).",
    func=_get_all_rps101_objects,
)

# Tool 2: Get Outcomes for an Object
class ObjectNameInput(BaseModel):
    object_name: str = Field(..., description="The name of the RPS-101 object to get winning outcomes for (e.g. 'nuke')")

def _get_rps101_object_outcomes(object_name: str) -> dict:
    response = requests.get(f"{BASE_URL}/objects/{object_name}")
    response.raise_for_status()
    return response.json()

get_rps101_object_outcomes = StructuredTool.from_function(
    name="get_rps101_object_outcomes",
    description="Get the winning outcomes for a given RPS-101 object. Returns what that object defeats and how.",
    func=_get_rps101_object_outcomes,
    args_schema=ObjectNameInput
)

# Tool 3: Match Two RPS-101 Objects
class RPSMatchInput(BaseModel):
    object_one: str = Field(..., description="The first object in the match (e.g. 'nuke')")
    object_two: str = Field(..., description="The second object in the match (e.g. 'tank')")

def _get_rps101_match_result(object_one: str, object_two: str) -> dict:
    response = requests.get(
        f"{BASE_URL}/match",
        params={"object_one": object_one, "object_two": object_two}
    )
    response.raise_for_status()
    return response.json()

get_rps101_match_result = StructuredTool.from_function(
    name="get_rps101_match_result",
    description="Get the result of a match between two RPS-101 objects.",
    func=_get_rps101_match_result,
    args_schema=RPSMatchInput
)

# Toolkit
class RPS101Toolkit(BaseToolkit):
    def get_tools(self) -> List[StructuredTool]:
        return [
            get_all_rps101_objects,
            get_rps101_object_outcomes,
            get_rps101_match_result
        ]
