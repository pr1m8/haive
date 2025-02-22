
from operator import add
from typing import Annotated, List

from typing_extensions import TypedDict
from pydantic import Field

class InputState(TypedDict):
    """
    Input state for the graph database agent.
    """
    question: str = Field(description="The user's question")


class OverallState(TypedDict):
    """
    Overall state for the graph database agent.
    """
    question: str = Field(description="The user's question")
    next_action: str = Field(description="The next action to take")
    cypher_statement: str = Field(description="The Cypher statement to execute")
    cypher_errors: List[str] = Field(description="The errors in the Cypher statement")
    database_records: List[dict] = Field(description="The records retrieved from the database")
    steps: Annotated[List[str], add] = Field(description="The steps taken to reach the current state")


class OutputState(TypedDict):
    """
    Output state for the graph database agent.
    """
    answer: str = Field(description="The answer to the user's question")
    steps: List[str] = Field(description="The steps taken to reach the current state")
    cypher_statement: str = Field(description="The Cypher statement to execute")

 