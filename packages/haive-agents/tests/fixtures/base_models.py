import operator
from typing import Annotated

from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field


class Plan(BaseModel):
    """A plan is a list of steps that are executed in order."""

    steps: list[str] = Field(description="The steps to execute")


class TestState(BaseModel):
    """ """

    messages: Annotated[list[AnyMessage], operator.add]
