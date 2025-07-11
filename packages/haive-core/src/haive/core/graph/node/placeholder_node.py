from typing import Union

from langgraph.types import Command
from pydantic import BaseModel

from haive.core.schema.state_schema import StateSchema


def placeholder_node(state: StateSchema | BaseModel) -> Command[None]:
    return Command(update={})
